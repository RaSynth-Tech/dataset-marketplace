"""ML utilities for agent operations."""
import logging
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from functools import lru_cache

logger = logging.getLogger(__name__)


class ModelCache:
    """Singleton cache for ML models to avoid reloading."""
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelCache, cls).__new__(cls)
        return cls._instance
    
    def get_sentence_transformer(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Get or load sentence transformer model."""
        if model_name not in self._models:
            logger.info(f"Loading sentence transformer model: {model_name}")
            self._models[model_name] = SentenceTransformer(model_name)
        return self._models[model_name]


def compute_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
    
    Returns:
        Similarity score between -1 and 1
    """
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def generate_embeddings(texts: List[str], model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings
        model_name: Name of the sentence transformer model
    
    Returns:
        Array of embeddings
    """
    cache = ModelCache()
    model = cache.get_sentence_transformer(model_name)
    return model.encode(texts, show_progress_bar=False)
