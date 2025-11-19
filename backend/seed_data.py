"""Script to seed sample data for development."""
from app.database import SessionLocal, engine, Base
from app.models.dataset import User, Dataset
from passlib.context import CryptContext
import random

# Create tables
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_data():
    db = SessionLocal()
    
    try:
        # Create sample users
        if db.query(User).count() == 0:
            # Create a buyer
            buyer = User(
                email="buyer@example.com",
                username="buyer",
                hashed_password=pwd_context.hash("password123"),
                full_name="John Buyer",
                balance=1000.0
            )
            db.add(buyer)
            
            # Create a seller
            seller = User(
                email="seller@example.com",
                username="seller",
                hashed_password=pwd_context.hash("password123"),
                full_name="Jane Seller",
                is_seller=True,
                balance=0.0
            )
            db.add(seller)
            
            db.commit()
            db.refresh(buyer)
            db.refresh(seller)
            
            print(f"Created users: buyer (ID: {buyer.id}), seller (ID: {seller.id})")
            
            # Create sample datasets
            sample_datasets = [
                {
                    "title": "E-commerce Sales Data 2023",
                    "description": "Comprehensive sales data from multiple e-commerce platforms including transaction details, customer demographics, and product categories.",
                    "category": "E-commerce",
                    "tags": ["sales", "transactions", "retail", "analytics"],
                    "price": 49.99,
                    "size_mb": 125.5,
                    "row_count": 50000,
                    "column_count": 15,
                    "format": "CSV",
                    "sample_data": {"sample": "data"},
                    "metadata": {"source": "aggregated", "period": "2023"}
                },
                {
                    "title": "Weather Data - Global Cities",
                    "description": "Daily weather data for 100+ global cities including temperature, humidity, precipitation, and wind speed.",
                    "category": "Weather",
                    "tags": ["weather", "climate", "temperature", "global"],
                    "price": 29.99,
                    "size_mb": 45.2,
                    "row_count": 36500,
                    "column_count": 8,
                    "format": "JSON",
                    "sample_data": {"sample": "data"},
                    "metadata": {"source": "weather_api", "period": "2022-2023"}
                },
                {
                    "title": "Social Media Sentiment Analysis",
                    "description": "Pre-processed sentiment analysis data from Twitter and Reddit posts across various topics.",
                    "category": "Social Media",
                    "tags": ["sentiment", "social", "nlp", "text"],
                    "price": 79.99,
                    "size_mb": 250.8,
                    "row_count": 100000,
                    "column_count": 5,
                    "format": "Parquet",
                    "sample_data": {"sample": "data"},
                    "metadata": {"source": "social_media", "processed": True}
                },
                {
                    "title": "Stock Market Historical Data",
                    "description": "Historical stock prices and trading volumes for S&P 500 companies from 2010-2023.",
                    "category": "Finance",
                    "tags": ["stocks", "finance", "trading", "historical"],
                    "price": 99.99,
                    "size_mb": 500.3,
                    "row_count": 200000,
                    "column_count": 10,
                    "format": "CSV",
                    "sample_data": {"sample": "data"},
                    "metadata": {"source": "market_data", "index": "S&P500"}
                },
                {
                    "title": "Customer Reviews Dataset",
                    "description": "Customer reviews and ratings for products across multiple categories with metadata.",
                    "category": "E-commerce",
                    "tags": ["reviews", "ratings", "customers", "products"],
                    "price": 39.99,
                    "size_mb": 78.6,
                    "row_count": 75000,
                    "column_count": 6,
                    "format": "JSON",
                    "sample_data": {"sample": "data"},
                    "metadata": {"source": "reviews", "verified": True}
                },
            ]
            
            for dataset_data in sample_datasets:
                dataset = Dataset(
                    **dataset_data,
                    seller_id=seller.id,
                    rating=round(random.uniform(3.5, 5.0), 1),
                    review_count=random.randint(10, 500),
                    download_count=random.randint(0, 1000)
                )
                db.add(dataset)
            
            db.commit()
            print(f"Created {len(sample_datasets)} sample datasets")
        else:
            print("Database already contains data. Skipping seed.")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

