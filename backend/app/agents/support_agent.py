"""Support agent for user assistance and queries."""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent


class SupportAgent(BaseAgent):
    """Agent responsible for providing user support and answering queries."""
    
    def __init__(self):
        super().__init__(
            name="SupportAgent",
            description="Provides user support and answers common questions"
        )
        self.faq_responses = {
            "pricing": "Dataset prices vary based on size, quality, and content. You can filter by price range in the search.",
            "download": "After purchase, you can download your dataset from the 'My Purchases' section.",
            "refund": "Refunds are available within 7 days of purchase if the dataset doesn't meet the description.",
            "format": "We support multiple formats including CSV, JSON, Parquet, and more. Check the dataset details for specific format.",
            "quality": "All datasets go through quality checks. Ratings and reviews help you make informed decisions.",
        }
    
    async def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user support queries.
        
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
        
        # Simple keyword matching (in production, use NLP/LLM)
        response = None
        suggestions = []
        
        for keyword, answer in self.faq_responses.items():
            if keyword in query:
                response = answer
                break
        
        if not response:
            # Generic response
            response = "I can help you with pricing, downloads, refunds, formats, and quality questions. What would you like to know?"
            suggestions = list(self.faq_responses.keys())
        else:
            # Suggest related topics
            suggestions = [k for k in self.faq_responses.keys() if k != keyword][:3]
        
        self.log(f"Processed support query: {query[:50]}")
        
        return {
            "response": response,
            "suggestions": suggestions,
            "query": query
        }
    
    def get_capabilities(self) -> List[str]:
        return ["faq_answering", "query_understanding", "suggestion_generation"]

