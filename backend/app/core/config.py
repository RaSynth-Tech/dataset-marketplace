import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Dataset Selling Platform"
    PROJECT_VERSION: str = "1.0.0"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dataset_platform")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")
    
    # Google Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
