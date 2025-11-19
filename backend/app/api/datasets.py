"""API endpoints for dataset operations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.dataset import DatasetResponse, DatasetSearch, DatasetCreate, DatasetUpdate
from app.agents.agent_orchestrator import AgentOrchestrator
from app.models.dataset import Dataset
import logging

router = APIRouter(prefix="/api/datasets", tags=["datasets"])
logger = logging.getLogger(__name__)

# Initialize orchestrator
orchestrator = AgentOrchestrator()


@router.get("/", response_model=List[DatasetResponse])
async def list_datasets(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all active datasets."""
    datasets = db.query(Dataset).filter(Dataset.is_active == True).offset(skip).limit(limit).all()
    return datasets


@router.get("/search", response_model=dict)
async def search_datasets(
    search_params: DatasetSearch = Depends(),
    db: Session = Depends(get_db)
):
    """Search datasets using the search agent."""
    result = await orchestrator.execute(
        "search",
        {
            "db": db,
            "search_params": search_params
        }
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Convert ORM objects to response models
    datasets = [DatasetResponse.model_validate(d) for d in result["datasets"]]
    
    return {
        "datasets": datasets,
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"]
    }


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a specific dataset by ID."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.get("/recommendations/{user_id}", response_model=dict)
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    """Get dataset recommendations for a user."""
    result = await orchestrator.execute(
        "recommendation",
        {
            "db": db,
            "user_id": user_id
        }
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    recommendations = [DatasetResponse.model_validate(d) for d in result["recommendations"]]
    
    return {
        "recommendations": recommendations,
        "count": result["count"]
    }


@router.post("/", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    # In production, add authentication
    # current_user: User = Depends(get_current_user)
):
    """Create a new dataset (seller only)."""
    # For demo, using seller_id = 1
    seller_id = 1
    
    db_dataset = Dataset(**dataset.dict(), seller_id=seller_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: int,
    dataset_update: DatasetUpdate,
    db: Session = Depends(get_db)
):
    """Update a dataset."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    update_data = dataset_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dataset, field, value)
    
    db.commit()
    db.refresh(dataset)
    return dataset

