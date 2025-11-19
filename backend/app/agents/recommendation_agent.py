"""Recommendation agent for suggesting datasets to users."""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.agents.base_agent import BaseAgent
from app.models.dataset import Dataset, Purchase


class RecommendationAgent(BaseAgent):
    """Agent responsible for recommending datasets to users."""
    
    def __init__(self):
        super().__init__(
            name="RecommendationAgent",
            description="Recommends datasets based on user behavior and preferences"
        )
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate dataset recommendations for a user.
        
        Args:
            input_data: Contains 'db' (database session) and 'user_id' (int)
            context: Optional context from search agent or other sources
            
        Returns:
            Dictionary with 'recommendations' (list of datasets)
        """
        db: Session = input_data.get("db")
        user_id: int = input_data.get("user_id")
        
        if not db:
            return {"error": "Missing database session", "recommendations": []}
        
        recommendations = []
        
        if user_id:
            # Get user's purchase history
            user_purchases = db.query(Purchase).filter(
                Purchase.buyer_id == user_id,
                Purchase.status == "completed"
            ).all()
            
            if user_purchases:
                # Collaborative filtering: find datasets similar to purchased ones
                purchased_categories = set()
                purchased_tags = set()
                
                for purchase in user_purchases:
                    dataset = purchase.dataset
                    if dataset.category:
                        purchased_categories.add(dataset.category)
                    if dataset.tags:
                        purchased_tags.update(dataset.tags)
                
                # Find similar datasets
                query = db.query(Dataset).filter(
                    Dataset.is_active == True,
                    Dataset.id.notin_([p.dataset_id for p in user_purchases])
                )
                
                if purchased_categories:
                    query = query.filter(Dataset.category.in_(purchased_categories))
                
                # Order by rating and relevance
                recommendations = query.order_by(
                    Dataset.rating.desc(),
                    Dataset.download_count.desc()
                ).limit(10).all()
        
        # If no user-specific recommendations, use popular datasets
        if not recommendations:
            recommendations = db.query(Dataset).filter(
                Dataset.is_active == True
            ).order_by(
                (Dataset.rating * 0.5 + (Dataset.download_count / 100) * 0.5).desc()
            ).limit(10).all()
        
        self.log(f"Generated {len(recommendations)} recommendations")
        
        return {
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    
    def get_capabilities(self) -> List[str]:
        return ["collaborative_filtering", "popular_datasets", "category_based", "tag_based"]

