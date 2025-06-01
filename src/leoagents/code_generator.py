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
                Generate a complete Leo program for: {requirements.project_name}

                PROJECT TYPE: {requirements.architecture.project_type}
                DESCRIPTION: {requirements.description}

                FEATURES TO IMPLEMENT:
                {chr(10).join(f"• {f}" for f in requirements.features)}

                REQUIRED DATA STRUCTURES:
                {chr(10).join(f"• {d}" for d in requirements.architecture.data_structures)}

                REQUIRED TRANSITIONS:
                {chr(10).join(f"• {t}" for t in requirements.architecture.transitions)}

                {f"ADMIN FEATURES:{chr(10)}{chr(10).join(f'• {a}' for a in requirements.architecture.admin_features)}" if requirements.architecture.admin_features else ""}

                You MUST generate the COMPLETE Leo code file content.
                The output should be a valid GeneratedCode object with:
                - project_name: "{requirements.project_name}"
                - code: <THE FULL LEO PROGRAM CODE>

                Start the code with: program {requirements.project_name}.aleo {{
                End with closing brace.

                GENERATE THE FULL LEO CODE NOW:
                """
            
            result = await Runner.run(agent, message)

            if result.final_output.code:
                return result.final_output
            else:
                input = result
                prompt = """Extract the Leo code from the previous response.
                
                Sometimes the code is embedded within explanatory text or formatted as user input.
                Your task is to:
                1. Identify the Leo program code within the response
                2. Extract ONLY the Leo code (starting with 'program' and ending with closing brace)
                3. Return it as a clean GeneratedCode object
                
                Focus only on extracting the actual Leo code, ignoring any surrounding text or explanations."""
                agentGetCode = Agent(
                    name="FixUserInputAgent",
                    instructions=prompt,
                    model='gpt-4.1-nano-2025-04-14',
                    output_type=GeneratedCode
                )
                result = await Runner.run(agentGetCode, input)
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