"""Search agent using Google Gemini for semantic search and external dataset discovery."""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.agents.base_agent import BaseAgent
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetSearch
from app.agents.gemini_utils import GeminiClient, compute_similarity
import logging
import json

logger = logging.getLogger(__name__)


class SearchAgent(BaseAgent):
    """Agent for semantic search using Google Gemini embeddings and external dataset discovery."""
    
    def __init__(self):
        super().__init__(
            name="SearchAgent",
            description="Searches datasets using Gemini AI embeddings and discovers external datasets"
        )
        self.gemini = GeminiClient()
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for datasets using Gemini semantic search and external sources.
        
        Args:
            input_data: Contains 'db' (database session) and 'search_params' (DatasetSearch)
            context: Optional context from other agents
            
        Returns:
            Dictionary with 'datasets' (list), 'external_datasets' (list), and 'total' (int)
        """
        db: Session = input_data.get("db")
        search_params: DatasetSearch = input_data.get("search_params")
        
        if not db or not search_params:
            return {"error": "Missing required parameters", "datasets": [], "total": 0}
        
        # Search local database
        query = db.query(Dataset).filter(Dataset.is_active == True)
        query = self._apply_filters(query, search_params)
        all_datasets = query.all()
        
        # If there's a text query, use Gemini for semantic ranking
        if search_params.query and all_datasets:
            try:
                ranked_datasets = self._gemini_semantic_ranking(search_params.query, all_datasets)
                self.log(f"Gemini semantic search: ranked {len(ranked_datasets)} datasets")
            except Exception as e:
                self.log(f"Gemini search failed: {e}, using fallback", level="warning")
                ranked_datasets = self._traditional_sorting(all_datasets, search_params.sort_by)
        else:
            ranked_datasets = self._traditional_sorting(all_datasets, search_params.sort_by)
        
        # Get external datasets using Gemini
        external_datasets = []
        if search_params.query:
            try:
                external_datasets = self._search_external_datasets(search_params.query)
                self.log(f"Found {len(external_datasets)} external datasets via Gemini")
            except Exception as e:
                self.log(f"External search failed: {e}", level="warning")
        
        # Pagination for local datasets
        total = len(ranked_datasets)
        offset = (search_params.page - 1) * search_params.page_size
        paginated_datasets = ranked_datasets[offset:offset + search_params.page_size]
        
        return {
            "datasets": paginated_datasets,
            "external_datasets": external_datasets[:5],  # Limit to 5 external results
            "total": total,
            "page": search_params.page,
            "page_size": search_params.page_size
        }
    
    def _search_external_datasets(self, query: str) -> List[Dict[str, Any]]:
        """
        Use Gemini to search for real datasets from online sources.
        
        Returns a list of external dataset suggestions with links.
        """
        prompt = f"""You are a dataset discovery assistant. Find real, publicly available datasets related to: "{query}"

Search across these sources:
- Kaggle (kaggle.com/datasets)
- UCI Machine Learning Repository (archive.ics.uci.edu/ml)
- Google Dataset Search (datasetsearch.research.google.com)
- Data.gov
- AWS Open Data Registry

Return EXACTLY 5 relevant datasets in this JSON format:
[
  {{
    "title": "Dataset Name",
    "description": "Brief description (1-2 sentences)",
    "source": "Source name (e.g., Kaggle, UCI ML)",
    "url": "Direct URL to dataset",
    "format": "CSV/JSON/Parquet/etc",
    "size_estimate": "Approximate size"
  }}
]

Return ONLY the JSON array, no other text."""

        try:
            response_text = self.gemini.generate_text(prompt, max_tokens=1000)
            
            # Extract JSON from response
            # Sometimes Gemini adds markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("[")
                json_end = response_text.rfind("]") + 1
                response_text = response_text[json_start:json_end]
            elif "```" in response_text:
                response_text = response_text.replace("```", "").strip()
            
            datasets = json.loads(response_text)
            return datasets if isinstance(datasets, list) else []
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"External dataset search failed: {e}")
            return []
    
    def _apply_filters(self, query, search_params: DatasetSearch):
        """Apply category, tag, price, and rating filters."""
        if search_params.category:
            query = query.filter(Dataset.category == search_params.category)
        
        if search_params.tags:
            for tag in search_params.tags:
                query = query.filter(Dataset.tags.contains([tag]))
        
        if search_params.min_price is not None:
            query = query.filter(Dataset.price >= search_params.min_price)
        if search_params.max_price is not None:
            query = query.filter(Dataset.price <= search_params.max_price)
        
        if search_params.min_rating is not None:
            query = query.filter(Dataset.rating >= search_params.min_rating)
        
        return query
    
    def _gemini_semantic_ranking(self, query_text: str, datasets: List[Dataset]) -> List[Dataset]:
        """
        Rank datasets using Gemini embeddings.
        
        Uses Google Gemini API to generate embeddings and compute semantic similarity.
        """
        # Generate query embedding
        query_embedding = self.gemini.generate_embedding(query_text)
        
        # Generate dataset embeddings and compute similarities
        similarities = []
        for dataset in datasets:
            dataset_text = f"{dataset.title}. {dataset.description}. Category: {dataset.category}. Tags: {', '.join(dataset.tags or [])}"
            dataset_embedding = self.gemini.generate_embedding(dataset_text)
            similarity = compute_similarity(query_embedding, dataset_embedding)
            similarities.append((dataset, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [dataset for dataset, _ in similarities]
    
    def _traditional_sorting(self, datasets: List[Dataset], sort_by: str) -> List[Dataset]:
        """Traditional sorting by price, rating, date, or relevance."""
        if sort_by == "price":
            return sorted(datasets, key=lambda d: d.price)
        elif sort_by == "rating":
            return sorted(datasets, key=lambda d: d.rating, reverse=True)
        elif sort_by == "date":
            return sorted(datasets, key=lambda d: d.created_at, reverse=True)
        else:  # relevance
            return sorted(
                datasets,
                key=lambda d: (d.rating * 0.6 + (d.download_count / 100) * 0.4),
                reverse=True
            )
    
    def get_capabilities(self) -> List[str]:
        return [
            "gemini_semantic_search",
            "external_dataset_discovery",
            "embedding_based_ranking",
            "category_filter",
            "tag_filter",
            "price_filter",
            "rating_filter",
            "sorting",
            "pagination"
        ]
