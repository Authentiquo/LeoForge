"""
Code Generator Agent - Generates Leo code from normalized requirements
"""
import os
from agents import Agent, Runner, trace
from agents.agent_output import AgentOutputSchema
from src.models import CodeRequirements, GeneratedCode, BuildResult
from src.config import get_config
from src.services.rule_manager import RuleManager
from .prompts import get_codegen_prompt, get_error_fix_prompt
from agents.extensions.models.litellm_model import LitellmModel
from rich import console
c = console.Console()

class CodeGeneratorAgent:
    """Agent responsible for generating Leo code from requirements"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_generator_model
        self.rule_manager = RuleManager()
    
    def _get_prompt_with_rules(self) -> str:
        """Get compact prompt with learned rules"""
        
        codex_rules = self.rule_manager.get_codex_rules(limit=3)
    
        rules = ""
        if codex_rules:
            for rule in codex_rules:
                rules += f"• {rule.title}: {rule.solution}\n"
        
        return get_codegen_prompt(self.config.admin_address, rules)
    
    async def generate_code(self, requirements: CodeRequirements) -> GeneratedCode:
        """Generate Leo code from requirements"""
        
        with trace("generate_code"):
            agent = Agent(
                name="CodeGeneratorAgent",
                instructions=self._get_prompt_with_rules(),
                model=LitellmModel(model=self.model, api_key=self.config.anthropic_api_key),
                output_type=GeneratedCode
            )
        
            message = f"""
            PROJECT: {requirements.project_name}
            TYPE: {requirements.architecture.project_type}
            DESCRIPTION: {requirements.description}

            FEATURES:
            {chr(10).join(f"• {f}" for f in requirements.features)}

            DATA STRUCTURES:
            {chr(10).join(f"• {d}" for d in requirements.architecture.data_structures)}

            TRANSITIONS:
            {chr(10).join(f"• {t}" for t in requirements.architecture.transitions)}

            {f"ADMIN FEATURES: {chr(10).join(f'• {a}' for a in requirements.architecture.admin_features)}" if requirements.architecture.admin_features else ""}

            Generate complete Leo code implementing all features.
"""
            
            result = await Runner.run(agent, message)
            
        return result.final_output
    


    async def fix_compilation_errors(self, 
                                   code: str, 
                                   build_result: BuildResult,
                                   requirements: CodeRequirements) -> GeneratedCode:
        """Fix compilation errors in existing code"""
        
        agent = Agent(
            name="CodeFixerAgent",
            instructions=self._get_prompt_with_rules(),
            model=LitellmModel(model=self.model, api_key=self.config.anthropic_api_key),
            output_type=GeneratedCode
        )
        
        message = get_error_fix_prompt().format(
            code=code,
            errors=build_result.stderr
        )
        
        result = await Runner.run(agent, message)
        
        return result.final_output