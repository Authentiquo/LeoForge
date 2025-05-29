"""
Code Evaluator Agent - Evaluates generated Leo code
"""
from agents import Agent, Runner
from src.models import CodeRequirements, GeneratedCode, EvaluationResult
from src.config import get_config
from .prompts import get_evaluator_prompt
from agents.extensions.models.litellm_model import LitellmModel

class CodeEvaluatorAgent:
    """Agent responsible for evaluating generated Leo code"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_evaluator_model
    
    async def evaluate_code(self, 
                          code: GeneratedCode, 
                          requirements: CodeRequirements) -> EvaluationResult:
        """Evaluate generated code against requirements"""
        
        agent = Agent(
            name="CodeEvaluatorAgent",
            instructions=get_evaluator_prompt(self.config.admin_address),
            model=LitellmModel(model=self.model, api_key=self.config.anthropic_api_key),
            output_type=EvaluationResult
        )
        
        # Simplified message
        message = f"""
        Evaluate this Leo code:

        PROJECT: {requirements.project_name}
        TYPE: {requirements.architecture.project_type}
        FEATURES: {', '.join(requirements.features)}
        {f"ADMIN FEATURES: {', '.join(requirements.architecture.admin_features)}" if requirements.architecture.admin_features else ""}
        REQUIRES ADMIN: {requirements.architecture.requires_admin}

        CODE:
        ```leo
        {code.code}
        ```

        Provide a fair and balanced evaluation. Give credit for correct implementation while noting areas for improvement.
        """
        
        result = await Runner.run(agent, message)
        return result.final_output 