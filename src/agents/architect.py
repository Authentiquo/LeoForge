"""
Architect Agent - Analyzes user queries and designs Leo project architecture
"""
from typing import Optional
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import UserQuery, ArchitectureDesign, ProjectType


class ArchitectAgent:
    """Agent responsible for analyzing user queries and creating project architecture"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-3-5-sonnet-20241022"):
        self.system_prompt = """
You are an expert Leo/Aleo blockchain architect.

Your role is to analyze user project requests and create detailed architecture designs.

RESPONSIBILITIES:
1. Understand the user's intent and project requirements
2. Identify the appropriate project type (token, NFT, DeFi, etc.)
3. Design data structures (records, structs)
4. Define transitions (functions) with clear signatures
5. Consider security implications
6. Ensure Leo syntax compliance

LEO SYNTAX REMINDERS:
- Programs: program name.aleo { ... }
- Records: record Name { owner: address, field: type }
- Transitions: transition name(param: type) -> type { ... }
- Types: u8, u16, u32, u64, u128, i8-i128, address, bool, field, scalar
- Privacy: private/public modifiers for inputs/outputs

OUTPUT FORMAT:
Create a comprehensive ArchitectureDesign with:
- Clear project name (lowercase, underscore separated)
- Accurate project type classification
- Detailed feature list
- Technical requirements
- Data structure definitions
- Transition signatures
- Security considerations

Be thorough but concise. Focus on creating a blueprint that a code generator can follow.
"""
        
        self.agent = Agent(
            name="ArchitectAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=AgentOutputSchema(ArchitectureDesign, strict_json_schema=False)
        )
    
    async def design_architecture(self, user_query: UserQuery) -> ArchitectureDesign:
        """Analyze user query and create project architecture"""
        
        message = f"""
USER REQUEST:
{user_query.query}

Project Type Hint: {user_query.project_type or "Auto-detect"}
Constraints: {', '.join(user_query.constraints) if user_query.constraints else "None specified"}

Please analyze this request and create a comprehensive architecture design for a Leo project.
Focus on:
1. Understanding the core functionality needed
2. Identifying all necessary data structures
3. Defining all required transitions
4. Considering security and best practices

Create the ArchitectureDesign output.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output 