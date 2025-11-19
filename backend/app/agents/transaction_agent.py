"""Transaction agent for handling purchases and payments."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.agents.base_agent import BaseAgent
from app.models.dataset import Dataset, User, Purchase


class TransactionAgent(BaseAgent):
    """Agent responsible for processing transactions and purchases."""
    
    def __init__(self):
        super().__init__(
            name="TransactionAgent",
            description="Handles dataset purchases and payment processing"
        )
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a dataset purchase.
        
        Args:
            input_data: Contains 'db' (database session), 'user_id' (int), 'dataset_id' (int)
            context: Optional context from other agents
            
        Returns:
            Dictionary with 'purchase' (Purchase object) and 'status' (str)
        """
        db: Session = input_data.get("db")
        user_id: int = input_data.get("user_id")
        dataset_id: int = input_data.get("dataset_id")
        
        if not db or not user_id or not dataset_id:
            return {"error": "Missing required parameters", "status": "failed"}
        
        # Get user and dataset
        user = db.query(User).filter(User.id == user_id).first()
        dataset = db.query(Dataset).filter(
            Dataset.id == dataset_id,
            Dataset.is_active == True
        ).first()
        
        if not user:
            return {"error": "User not found", "status": "failed"}
        
        if not dataset:
            return {"error": "Dataset not found or inactive", "status": "failed"}
        
        # Check if user already purchased this dataset
        existing_purchase = db.query(Purchase).filter(
            Purchase.buyer_id == user_id,
            Purchase.dataset_id == dataset_id,
            Purchase.status == "completed"
        ).first()
        
        if existing_purchase:
            return {
                "error": "Dataset already purchased",
                "status": "failed",
                "purchase": existing_purchase
            }
        
        # Check user balance (in a real system, integrate with payment gateway)
        if user.balance < dataset.price:
            return {
                "error": "Insufficient balance",
                "status": "failed",
                "required": dataset.price,
                "available": user.balance
            }
        
        # Create purchase record
        transaction_id = str(uuid.uuid4())
        purchase = Purchase(
            buyer_id=user_id,
            dataset_id=dataset_id,
            amount=dataset.price,
            transaction_id=transaction_id,
            status="pending"
        )
        
        db.add(purchase)
        
        # Deduct balance and update seller balance
        user.balance -= dataset.price
        seller = dataset.seller
        if seller:
            seller.balance += dataset.price
        
        # Update dataset download count
        dataset.download_count += 1
        
        # Complete transaction
        purchase.status = "completed"
        db.commit()
        db.refresh(purchase)
        
        self.log(f"Purchase completed: {transaction_id} for dataset {dataset_id} by user {user_id}")
        
        return {
            "purchase": purchase,
            "status": "completed",
            "transaction_id": transaction_id
        }
    
    def get_capabilities(self) -> List[str]:
        return ["purchase_processing", "balance_management", "duplicate_check", "transaction_tracking"]

