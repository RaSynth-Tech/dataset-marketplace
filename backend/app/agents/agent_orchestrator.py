"""Agent orchestrator for coordinating multiple agents."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.search_agent import SearchAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.transaction_agent import TransactionAgent
from app.agents.support_agent import SupportAgent
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrates multiple agents to handle complex tasks."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {
            "search": SearchAgent(),
            "recommendation": RecommendationAgent(),
            "transaction": TransactionAgent(),
            "support": SupportAgent()
        }
        self.logger = logging.getLogger(f"{__name__}.AgentOrchestrator")
    
    async def execute(self, task: str, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a task using the appropriate agent(s).
        
        Args:
            task: Task name (search, recommend, purchase, support)
            input_data: Input data for the task
            context: Optional context from previous operations
            
        Returns:
            Result from agent execution
        """
        agent = self.agents.get(task.lower())
        
        if not agent:
            return {"error": f"Unknown task: {task}", "available_tasks": list(self.agents.keys())}
        
        try:
            result = await agent.process(input_data, context)
            self.logger.info(f"Task '{task}' executed successfully by {agent.name}")
            return result
        except Exception as e:
            self.logger.error(f"Error executing task '{task}': {str(e)}")
            return {"error": str(e), "task": task}
    
    async def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a workflow of multiple agent tasks.
        
        Args:
            workflow: List of task definitions, each with 'task', 'input_data', and optionally 'use_result_as_context'
            
        Returns:
            Combined results from all tasks
        """
        results = {}
        context = {}
        
        for step in workflow:
            task = step.get("task")
            input_data = step.get("input_data", {})
            use_result = step.get("use_result_as_context", False)
            
            # Merge context into input_data if needed
            if use_result and context:
                input_data.update(context)
            
            result = await self.execute(task, input_data, context)
            results[task] = result
            
            # Update context for next steps
            if use_result:
                context.update(result)
        
        return results
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents."""
        return {
            name: agent.get_capabilities()
            for name, agent in self.agents.items()
        }
    
    def list_agents(self) -> List[str]:
        """List all available agents."""
        return list(self.agents.keys())

