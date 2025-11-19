"""API endpoints for purchase operations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.dataset import PurchaseCreate, PurchaseResponse
from app.agents.agent_orchestrator import AgentOrchestrator
from app.models.dataset import Purchase, User
import logging

router = APIRouter(prefix="/api/purchases", tags=["purchases"])
logger = logging.getLogger(__name__)

# Initialize orchestrator
orchestrator = AgentOrchestrator()


@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    # In production, get from authentication
    user_id: int = 1
):
    """Purchase a dataset using the transaction agent."""
    result = await orchestrator.execute(
        "transaction",
        {
            "db": db,
            "user_id": user_id,
            "dataset_id": purchase.dataset_id
        }
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Purchase failed: {result.get('error', 'Unknown error')}")
    
    return PurchaseResponse.model_validate(result["purchase"])


@router.get("/user/{user_id}", response_model=List[PurchaseResponse])
async def get_user_purchases(user_id: int, db: Session = Depends(get_db)):
    """Get all purchases for a user."""
    purchases = db.query(Purchase).filter(
        Purchase.buyer_id == user_id
    ).order_by(Purchase.purchased_at.desc()).all()
    return purchases


@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    """Get a specific purchase by ID."""
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

