"""
Code Evaluator Agent - Evaluates generated Leo code for completeness and quality
"""
import json
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import GeneratedCode, CodeRequirements, EvaluationResult
from .prompt import CODE_EVALUATOR_SYSTEM_PROMPT, CODE_EVALUATOR_MESSAGE_TEMPLATE


class CodeEvaluatorAgent:
    """Agent responsible for evaluating generated Leo code"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-sonnet-4-20250514"):
        self.system_prompt = CODE_EVALUATOR_SYSTEM_PROMPT
        
        
        output_schema = AgentOutputSchema(
            output_type=EvaluationResult,
            strict_json_schema=False
        )
        
        self.agent = Agent(
            name="CodeEvaluatorAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=output_schema
        )
    
    async def evaluate_code(self, 
                          generated_code: GeneratedCode,
                          requirements: CodeRequirements) -> EvaluationResult:
        """Evaluate generated code against requirements"""
        
        message = CODE_EVALUATOR_MESSAGE_TEMPLATE.format(
            project_name=requirements.project_name,
            project_type=requirements.architecture.project_type,
            features=', '.join(requirements.features),
            technical_requirements=', '.join(requirements.architecture.technical_requirements),
            security_considerations=', '.join(requirements.architecture.security_considerations),
            code=generated_code.code
        )
        
        result = await Runner.run(self.agent, message)
        
        # Return the structured output directly
        return result.final_output 