"""
Architect Agent - Analyzes user queries and designs Leo project architecture
"""
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import UserQuery, ArchitectureDesign
from .prompt import ARCHITECT_SYSTEM_PROMPT, ARCHITECT_MESSAGE_TEMPLATE


class ArchitectAgent:
    """Agent responsible for analyzing user queries and creating project architecture"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-3-7-sonnet-20250219"):
        self.system_prompt = ARCHITECT_SYSTEM_PROMPT
        
    
        output_schema = AgentOutputSchema(
            output_type=ArchitectureDesign,
            strict_json_schema=False
        )
        
        self.agent = Agent(
            name="ArchitectAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=output_schema,
        )
    
    async def design_architecture(self, user_query: UserQuery) -> ArchitectureDesign:
        """Analyze user query and create project architecture"""
        
        message = ARCHITECT_MESSAGE_TEMPLATE.format(
            query=user_query.query,
            project_type=user_query.project_type or "Auto-detect",
            constraints=', '.join(user_query.constraints) if user_query.constraints else "None specified"
        )
        
        result = await Runner.run(self.agent, message)
        return result.final_output 