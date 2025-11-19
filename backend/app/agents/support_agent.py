"""Support agent using Google Gemini for conversational AI."""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.agents.gemini_utils import GeminiClient
import logging

logger = logging.getLogger(__name__)


class SupportAgent(BaseAgent):
    """Agent for conversational support using Google Gemini."""
    
    def __init__(self):
        super().__init__(
            name="SupportAgent",
            description="Provides conversational AI support using Gemini"
        )
        self.gemini = GeminiClient()
        
        # FAQ for quick responses
        self.faq_responses = {
            "pricing": "Dataset prices vary based on size, quality, and content. You can filter by price range in the search.",
            "download": "After purchase, you can download your dataset from the 'My Purchases' section.",
            "refund": "Refunds are available within 7 days of purchase if the dataset doesn't meet the description.",
            "format": "We support multiple formats including CSV, JSON, Parquet, and more. Check the dataset details for specific format.",
            "quality": "All datasets go through quality checks. Ratings and reviews help you make informed decisions.",
        }
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user support queries using Gemini AI.
        
        Args:
            input_data: Contains 'query' (str) - user's question
            context: Optional context from other agents
            
        Returns:
            Dictionary with 'response' (str) and 'suggestions' (list)
        """
        query: str = input_data.get("query", "").lower()
        
        if not query:
            return {
                "response": "How can I help you today?",
                "suggestions": list(self.faq_responses.keys())
            }
        
        # Check FAQ first for instant responses
        faq_response = self._check_faq(query)
        if faq_response:
            self.log("Answered using FAQ")
            return {
                "response": faq_response,
                "suggestions": self._get_related_topics(query),
                "source": "faq"
            }
        
        # Use Gemini for complex queries
        try:
            ai_response = self._generate_gemini_response(query)
            self.log("Generated Gemini AI response")
            return {
                "response": ai_response,
                "suggestions": [],
                "source": "gemini"
            }
        except Exception as e:
            self.log(f"Gemini response failed: {e}, using generic fallback", level="warning")
            return {
                "response": "I can help you with pricing, downloads, refunds, formats, and quality questions. What would you like to know?",
                "suggestions": list(self.faq_responses.keys()),
                "source": "fallback"
            }
    
    def _check_faq(self, query: str) -> Optional[str]:
        """Check if query matches FAQ keywords."""
        for keyword, answer in self.faq_responses.items():
            if keyword in query:
                return answer
        return None
    
    def _generate_gemini_response(self, query: str) -> str:
        """
        Generate response using Google Gemini.
        
        Uses Gemini's conversational capabilities to provide helpful, contextual answers.
        """
        prompt = f"""You are a helpful support agent for a dataset marketplace platform.

Platform Features:
- Users can browse and search for datasets
- Datasets can be purchased using account balance
- Purchased datasets can be downloaded from "My Purchases"
- Datasets have categories, tags, ratings, and reviews
- Users need to be logged in to purchase datasets

User Question: {query}

Provide a helpful, concise answer (2-3 sentences). Be friendly and professional."""
        
        response = self.gemini.generate_text(prompt, max_tokens=200)
        return response.strip()
    
    def _get_related_topics(self, query: str) -> List[str]:
        """Get related FAQ topics."""
        related = [k for k in self.faq_responses.keys() if k not in query]
        return related[:3]
    
    def get_capabilities(self) -> List[str]:
        return [
            "faq_answering",
            "gemini_conversational_ai",
            "query_understanding",
            "suggestion_generation",
            "contextual_responses"
        ]
