"""Dataset model."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Dataset(Base):
    """Dataset model for storing dataset information."""
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), index=True)
    tags = Column(JSON, default=list)  # List of tags
    price = Column(Float, nullable=False)
    size_mb = Column(Float, nullable=False)
    row_count = Column(Integer)
    column_count = Column(Integer)
    format = Column(String(50))  # CSV, JSON, Parquet, etc.
    sample_data = Column(JSON)  # Sample rows for preview
    metadata = Column(JSON, default=dict)  # Additional metadata
    file_path = Column(String(500))  # Path to actual dataset file
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    download_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    seller = relationship("User", back_populates="datasets")
    purchases = relationship("Purchase", back_populates="dataset")


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_seller = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    datasets = relationship("Dataset", back_populates="seller")
    purchases = relationship("Purchase", back_populates="buyer")


class Purchase(Base):
    """Purchase transaction model."""
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String(255), unique=True, index=True)
    status = Column(String(50), default="pending")  # pending, completed, failed
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())

    buyer = relationship("User", back_populates="purchases")
    dataset = relationship("Dataset", back_populates="purchases")

