"""API endpoints for support operations."""
from fastapi import APIRouter, Depends, HTTPException
from app.agents.agent_orchestrator import AgentOrchestrator
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/api/support", tags=["support"])
logger = logging.getLogger(__name__)

# Initialize orchestrator
orchestrator = AgentOrchestrator()


class SupportQuery(BaseModel):
    """Schema for support query."""
    query: str


@router.post("/query")
async def handle_support_query(query: SupportQuery):
    """Handle user support queries using the support agent."""
    result = await orchestrator.execute(
        "support",
        {
            "query": query.query
        }
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

