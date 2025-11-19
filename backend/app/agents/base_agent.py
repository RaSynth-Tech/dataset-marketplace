"""Base agent class for multi-agent system."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input data and return result.
        
        Args:
            input_data: Input data for processing
            context: Optional context from other agents or system
            
        Returns:
            Dictionary with processing results
        """
        pass
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides."""
        return []
    
    def log(self, message: str, level: str = "info"):
        """Log a message."""
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message)

