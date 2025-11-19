"""Search agent for finding relevant datasets."""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.agents.base_agent import BaseAgent
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetSearch


class SearchAgent(BaseAgent):
    """Agent responsible for searching and retrieving datasets."""
    
    def __init__(self):
        super().__init__(
            name="SearchAgent",
            description="Searches and retrieves datasets based on user queries"
        )
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for datasets based on query parameters.
        
        Args:
            input_data: Contains 'db' (database session) and 'search_params' (DatasetSearch)
            context: Optional context from other agents
            
        Returns:
            Dictionary with 'datasets' (list) and 'total' (int)
        """
        db: Session = input_data.get("db")
        search_params: DatasetSearch = input_data.get("search_params")
        
        if not db or not search_params:
            return {"error": "Missing required parameters", "datasets": [], "total": 0}
        
        # Build query
        query = db.query(Dataset).filter(Dataset.is_active == True)
        
        # Text search
        if search_params.query:
            search_term = f"%{search_params.query.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Dataset.title).like(search_term),
                    func.lower(Dataset.description).like(search_term),
                    func.lower(Dataset.category).like(search_term)
                )
            )
        
        # Category filter
        if search_params.category:
            query = query.filter(Dataset.category == search_params.category)
        
        # Tags filter
        if search_params.tags:
            # PostgreSQL JSONB contains check
            for tag in search_params.tags:
                query = query.filter(Dataset.tags.contains([tag]))
        
        # Price range
        if search_params.min_price is not None:
            query = query.filter(Dataset.price >= search_params.min_price)
        if search_params.max_price is not None:
            query = query.filter(Dataset.price <= search_params.max_price)
        
        # Rating filter
        if search_params.min_rating is not None:
            query = query.filter(Dataset.rating >= search_params.min_rating)
        
        # Sorting
        if search_params.sort_by == "price":
            query = query.order_by(Dataset.price.asc())
        elif search_params.sort_by == "rating":
            query = query.order_by(Dataset.rating.desc())
        elif search_params.sort_by == "date":
            query = query.order_by(Dataset.created_at.desc())
        else:  # relevance (default)
            # Simple relevance: combination of rating and download count
            query = query.order_by(
                (Dataset.rating * 0.6 + (Dataset.download_count / 100) * 0.4).desc()
            )
        
        # Get total count
        total = query.count()
        
        # Pagination
        offset = (search_params.page - 1) * search_params.page_size
        datasets = query.offset(offset).limit(search_params.page_size).all()
        
        self.log(f"Found {total} datasets matching search criteria")
        
        return {
            "datasets": datasets,
            "total": total,
            "page": search_params.page,
            "page_size": search_params.page_size
        }
    
    def get_capabilities(self) -> List[str]:
        return ["text_search", "category_filter", "tag_filter", "price_filter", "rating_filter", "sorting", "pagination"]

