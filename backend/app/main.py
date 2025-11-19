"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.api import datasets, purchases, support, users, auth

# ... (logging config)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dataset Selling Platform",
    description="A scalable platform for buying and selling datasets with multi-agent system",
    version="1.0.0"
)

# Session Middleware (Required for Authlib)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(purchases.router)
app.include_router(support.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Dataset Selling Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

