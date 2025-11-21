"""API endpoints for dataset operations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.dataset import DatasetResponse, DatasetSearch, DatasetCreate, DatasetUpdate
from app.agents.agent_orchestrator import AgentOrchestrator
from app.models.dataset import Dataset, User
from app.api.deps import get_current_user
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
        "external_datasets": result.get("external_datasets", []),
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"]
    }


@router.get("/recommendations", response_model=dict)
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dataset recommendations for the current user."""
    result = await orchestrator.execute(
        "recommendation",
        {
            "db": db,
            "user_id": current_user.id
        }
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    recommendations = [DatasetResponse.model_validate(d) for d in result["recommendations"]]
    
    return {
        "recommendations": recommendations,
        "external_recommendations": result.get("external_recommendations", []),
        "count": result["count"]
    }


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a specific dataset by ID."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset



@router.post("/", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new dataset (seller only)."""
    # In a real app, check if current_user.is_seller
    
    dataset_data = dataset.model_dump()
    metadata_payload = dataset_data.pop("metadata", None)
    db_dataset = Dataset(
        **dataset_data,
        metadata_json=metadata_payload or {},
        seller_id=current_user.id
    )
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
    metadata_payload = update_data.pop("metadata", None)
    for field, value in update_data.items():
        setattr(dataset, field, value)
    if metadata_payload is not None:
        dataset.metadata_json = metadata_payload
    
    db.commit()
    db.refresh(dataset)
    return dataset

