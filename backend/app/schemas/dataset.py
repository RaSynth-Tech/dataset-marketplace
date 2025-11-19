"""Pydantic schemas for dataset operations."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetBase(BaseModel):
    """Base dataset schema."""
    title: str
    description: str
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    price: float
    size_mb: float
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    format: Optional[str] = None
    sample_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = {}


class DatasetCreate(DatasetBase):
    """Schema for creating a dataset."""
    pass


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None


class DatasetResponse(DatasetBase):
    """Schema for dataset response."""
    id: int
    seller_id: int
    is_active: bool
    download_count: int
    rating: float
    review_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DatasetSearch(BaseModel):
    """Schema for dataset search."""
    query: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    sort_by: Optional[str] = "relevance"  # relevance, price, rating, date
    page: int = 1
    page_size: int = 20


class UserCreate(BaseModel):
    """Schema for user creation."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_seller: bool
    balance: float
    created_at: datetime

    model_config = {"from_attributes": True}


class PurchaseCreate(BaseModel):
    """Schema for purchase creation."""
    dataset_id: int


class PurchaseResponse(BaseModel):
    """Schema for purchase response."""
    id: int
    buyer_id: int
    dataset_id: int
    amount: float
    transaction_id: str
    status: str
    purchased_at: datetime

    model_config = {"from_attributes": True}

