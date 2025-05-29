"""
Architect Agent - Analyzes user queries and designs Leo project architecture
"""
from itertools import tee
import os
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import UserQuery, ArchitectureDesign
from src.config import get_config
from src.services.rule_manager import RuleManager
from .prompts import get_architect_prompt
from agents.extensions.models.litellm_model import LitellmModel

class ArchitectAgent:
    """Agent responsible for analyzing user queries and creating project architecture"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_architect_model
        self.rule_manager = RuleManager()
        
    def _get_prompt_with_rules(self) -> str:
        """Get compact prompt with learned rules"""
        architect_rules = self.rule_manager.get_architect_rules(limit=3)
        rules = ""
        if architect_rules:
            for rule in architect_rules:
                rules += f"• {rule.title}: {rule.solution}\n"
        
        return get_architect_prompt(self.config.admin_address, rules)
    
    async def design_architecture(self, user_query: UserQuery) -> ArchitectureDesign:
        """Analyze user query and create project architecture"""
        
        # Create agent with compact prompt
        agent = Agent(
            name="ArchitectAgent",
            instructions=self._get_prompt_with_rules(),
            model=LitellmModel(model=self.model, api_key=self.config.anthropic_api_key),
            output_type=ArchitectureDesign
        )
        
        # Simplified message format
        message = f"""
            USER REQUEST: {user_query.query}
            Type: {user_query.project_type or "Auto-detect"}
            Constraints: {', '.join(user_query.constraints) if user_query.constraints else "None"}

            Create minimal architecture design focusing on core functionality only.
            """
        
        result = await Runner.run(agent, message)
        return result.final_output 
