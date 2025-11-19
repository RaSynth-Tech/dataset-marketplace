"""Gemini AI utilities for agent operations."""
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from app.core.config import settings
import os

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.warning("GEMINI_API_KEY not set. Gemini features will use fallback responses.")


class GeminiClient:
    """Singleton client for Google Gemini API."""
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
        return cls._instance
    
    def get_model(self, model_name: str = 'gemini-2.5-flash'):
        """Get or create Gemini model instance."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
            
        if self._model is None:
            logger.info(f"Initializing Gemini model: {model_name}")
            self._model = genai.GenerativeModel(model_name)
        return self._model
    
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using Gemini.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated text
        """
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
            
        try:
            model = self.get_model()
            # Generate content without custom config to avoid multi-part responses
            response = model.generate_content(prompt)
            
            # Return response text
            return response.text
                
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using Gemini.
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector
        """
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Gemini embedding failed: {e}")
            raise


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
    
    Returns:
        Similarity score between -1 and 1
    """
    import math
    
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(a * a for a in embedding1))
    magnitude2 = math.sqrt(sum(b * b for b in embedding2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
