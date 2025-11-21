"""Recommendation agent using Google Gemini for intelligent recommendations."""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.agents.base_agent import BaseAgent
from app.models.dataset import Dataset, Purchase
from app.agents.gemini_utils import GeminiClient
import logging
import json

logger = logging.getLogger(__name__)


class RecommendationAgent(BaseAgent):
    """Agent for AI-powered recommendations using Google Gemini."""
    
    def __init__(self):
        super().__init__(
            name="RecommendationAgent",
            description="Recommends datasets using Gemini AI analysis from local and online sources"
        )
        self.gemini = GeminiClient()
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate AI-powered recommendations using Gemini from local and external sources.
        
        Args:
            input_data: Contains 'db' (database session) and 'user_id' (int)
            context: Optional context from search agent or other sources
            
        Returns:
            Dictionary with 'recommendations' (list of local datasets) and 'external_recommendations' (list)
        """
        db: Session = input_data.get("db")
        user_id: int = input_data.get("user_id")
        
        if not db:
            return {"error": "Missing database session", "recommendations": [], "external_recommendations": []}
        
        local_recommendations = []
        external_recommendations = []
        
        if user_id:
            # Get local recommendations
            try:
                local_recommendations = self._gemini_recommendations(db, user_id)
                self.log(f"Gemini local recommendations generated: {len(local_recommendations)} items")
            except Exception as e:
                self.log(f"Gemini recommendation failed: {e}, using fallback", level="warning")
                local_recommendations = self._content_based_recommendations(db, user_id)
            
            # Get external recommendations based on user interests
            try:
                user_interests = self._extract_user_interests(db, user_id)
                if user_interests:
                    external_recommendations = self._recommend_external_datasets(user_interests)
                    self.log(f"Found {len(external_recommendations)} external recommendations via Gemini")
            except Exception as e:
                self.log(f"External recommendations failed: {e}", level="warning")
        else:
            local_recommendations = self._popular_datasets(db)
        
        return {
            "recommendations": local_recommendations[:10],
            "external_recommendations": external_recommendations[:5],
            "count": len(local_recommendations[:10])
        }
    
    def _extract_user_interests(self, db: Session, user_id: int) -> str:
        """Extract user interests from purchase history."""
        user_purchases = db.query(Purchase).filter(
            Purchase.buyer_id == user_id,
            Purchase.status == "completed"
        ).all()
        
        if not user_purchases:
            # Default interests for new users to enable external recommendations
            return "General data science, economics, machine learning, and public datasets."
        
        categories = set()
        tags = set()
        titles = []
        
        for purchase in user_purchases:
            dataset = purchase.dataset
            if dataset.category:
                categories.add(dataset.category)
            if dataset.tags:
                tags.update(dataset.tags[:3])  # Limit tags
            titles.append(dataset.title)
        
        interests = f"Categories: {', '.join(categories)}. "
        interests += f"Tags: {', '.join(list(tags)[:10])}. "
        interests += f"Previously purchased: {', '.join(titles[:3])}"
        
        return interests
    
    def _recommend_external_datasets(self, user_interests: str) -> List[Dict[str, Any]]:
        """
        Use Gemini to recommend external datasets based on user interests.
        
        Returns a list of external dataset recommendations with links.
        """
        prompt = f"""You are a dataset recommendation expert. Based on the user's interests, recommend real, publicly available datasets they might like.

User Interests:
{user_interests}

Find datasets from these sources:
- Kaggle
- UCI Machine Learning Repository
- Google Dataset Search
- Data.gov
- AWS Open Data Registry
- HuggingFace Datasets

Return EXACTLY 5 relevant dataset recommendations in this JSON format:
[
  {{
    "title": "Dataset Name",
    "description": "Why this matches user interests (2-3 sentences)",
    "source": "Source name (e.g., Kaggle, UCI ML)",
    "url": "URL to the SEARCH PAGE for this dataset (e.g., https://www.kaggle.com/search?q=dataset+name)",
    "format": "CSV/JSON/Parquet/etc",
    "size_estimate": "Approximate size",
    "relevance_score": "High/Medium (based on user interests)"
  }}
]

IMPORTANT: Do NOT guess specific dataset URLs as they might be broken. ALWAYS provide a search URL for the repository that will likely contain the dataset.
Return ONLY the JSON array, no other text."""

        try:
            response_text = self.gemini.generate_text(prompt, max_tokens=1200)
            
            # Extract JSON from response
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
            logger.error(f"External dataset recommendation failed: {e}")
            # Fallback for demo/quota exceeded
            return [
                {
                    "title": "Stock Market Data (Mock)",
                    "description": "Historical stock prices (Fallback due to API quota).",
                    "source": "Kaggle",
                    "url": "https://www.kaggle.com/search?q=stock+market+data",
                    "format": "CSV",
                    "size_estimate": "100MB",
                    "relevance_score": "High"
                },
                {
                    "title": "Global Economic Indicators (Mock)",
                    "description": "GDP and inflation data.",
                    "source": "World Bank",
                    "url": "https://data.worldbank.org/indicator",
                    "format": "CSV",
                    "size_estimate": "50MB",
                    "relevance_score": "Medium"
                }
            ]
    
    def _gemini_recommendations(self, db: Session, user_id: int) -> List[Dataset]:
        """
        Use Gemini to analyze user preferences and recommend local datasets.
        
        This uses Gemini's reasoning capabilities to understand user preferences.
        """
        # Get user's purchase history
        user_purchases = db.query(Purchase).filter(
            Purchase.buyer_id == user_id,
            Purchase.status == "completed"
        ).all()
        
        if not user_purchases:
            return self._popular_datasets(db)
        
        # Build user profile from purchases
        purchased_datasets = [p.dataset for p in user_purchases]
        user_profile = self._build_user_profile(purchased_datasets)
        
        # Get all available datasets (not purchased)
        available_datasets = db.query(Dataset).filter(
            Dataset.is_active == True,
            Dataset.id.notin_([p.dataset_id for p in user_purchases])
        ).limit(50).all()  # Limit to avoid too many API calls
        
        if not available_datasets:
            return []
        
        # Use Gemini to rank datasets based on user profile
        prompt = f"""You are a dataset recommendation expert. 

User's Purchase History:
{user_profile}

Available Datasets:
{self._format_datasets_for_prompt(available_datasets)}

Task: Recommend the top 10 datasets that best match the user's interests based on their purchase history.
Return ONLY the dataset IDs as a comma-separated list (e.g., "5,12,3,8,15,22,1,9,17,11").
"""
        
        try:
            response = self.gemini.generate_text(prompt, max_tokens=100)
            recommended_ids = self._parse_recommendation_response(response)
            
            # Fetch recommended datasets in order
            recommendations = []
            for dataset_id in recommended_ids:
                dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
                if dataset:
                    recommendations.append(dataset)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Gemini recommendation parsing failed: {e}")
            return self._content_based_recommendations(db, user_id)
    
    def _build_user_profile(self, datasets: List[Dataset]) -> str:
        """Build a text profile of user's interests."""
        categories = set()
        tags = set()
        
        for dataset in datasets:
            if dataset.category:
                categories.add(dataset.category)
            if dataset.tags:
                tags.update(dataset.tags)
        
        return f"Categories: {', '.join(categories)}. Tags: {', '.join(list(tags)[:10])}"
    
    def _format_datasets_for_prompt(self, datasets: List[Dataset]) -> str:
        """Format datasets for Gemini prompt."""
        formatted = []
        for d in datasets[:20]:  # Limit to avoid token limits
            formatted.append(
                f"ID:{d.id} - {d.title} (Category: {d.category}, Tags: {', '.join(d.tags[:3] if d.tags else [])})"
            )
        return "\n".join(formatted)
    
    def _parse_recommendation_response(self, response: str) -> List[int]:
        """Parse Gemini response to extract dataset IDs."""
        # Extract numbers from response
        import re
        numbers = re.findall(r'\d+', response)
        return [int(n) for n in numbers[:10]]
    
    def _content_based_recommendations(self, db: Session, user_id: int) -> List[Dataset]:
        """Fallback: content-based filtering."""
        user_purchases = db.query(Purchase).filter(
            Purchase.buyer_id == user_id,
            Purchase.status == "completed"
        ).all()
        
        if not user_purchases:
            return self._popular_datasets(db)
        
        # Extract categories
        purchased_categories = set()
        for purchase in user_purchases:
            if purchase.dataset.category:
                purchased_categories.add(purchase.dataset.category)
        
        # Find similar datasets
        query = db.query(Dataset).filter(
            Dataset.is_active == True,
            Dataset.id.notin_([p.dataset_id for p in user_purchases])
        )
        
        if purchased_categories:
            query = query.filter(Dataset.category.in_(purchased_categories))
        
        return query.order_by(
            Dataset.rating.desc(),
            Dataset.download_count.desc()
        ).limit(10).all()
    
    def _popular_datasets(self, db: Session) -> List[Dataset]:
        """Fallback: return popular datasets."""
        return db.query(Dataset).filter(
            Dataset.is_active == True
        ).order_by(
            (Dataset.rating * 0.5 + (Dataset.download_count / 100) * 0.5).desc()
        ).limit(10).all()
    
    def get_capabilities(self) -> List[str]:
        return [
            "gemini_ai_recommendations",
            "external_dataset_recommendations",
            "user_preference_analysis",
            "content_based_filtering",
            "popular_datasets"
        ]
