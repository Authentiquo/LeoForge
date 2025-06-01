"""
Code Generator Agent - Generates Leo code from normalized requirements
"""
import os
from anthropic import AsyncAnthropic
from src.models import CodeRequirements, GeneratedCode, BuildResult
from src.config import get_config
from src.services.rule_manager import RuleManager
from .prompts import get_codegen_prompt, get_error_fix_prompt
from rich import console
c = console.Console()

class CodeGeneratorAgent:
    """Agent responsible for generating Leo code from requirements"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_generator_model
        self.rule_manager = RuleManager()
        self.client = AsyncAnthropic(api_key=self.config.anthropic_api_key)
        self.max_tokens = 6000
    
    def _format_leo_code(self, code: str) -> str:
        """Format Leo code by replacing literal \n with actual newlines"""
        # Replace literal \n with actual newlines
        formatted_code = code.replace('\\n', '\n')
        
        # Clean up any double newlines that might have been created
        while '\n\n\n' in formatted_code:
            formatted_code = formatted_code.replace('\n\n\n', '\n\n')
        
        # Ensure proper spacing around braces
        formatted_code = formatted_code.replace('}{', '}\n{')
        
        return formatted_code.strip()
    
    def _get_prompt_with_rules(self) -> str:
        """Get compact prompt with learned rules"""
        
        codex_rules = self.rule_manager.get_codex_rules(limit=3)
    
        rules = ""
        if codex_rules:
            for rule in codex_rules:
                rules += f"• {rule.title}: {rule.solution}\n"
        
        return get_codegen_prompt(self.config.admin_address, rules)
    
    def _extract_leo_code_from_text(self, content: str) -> str:
        """Extract Leo code from text content"""
        # Look for code blocks first
        if "```" in content:
            lines = content.split('\n')
            in_code_block = False
            code_lines = []
            
            for line in lines:
                if line.strip().startswith('```'):
                    if in_code_block:
                        break  # End of code block
                    else:
                        in_code_block = True  # Start of code block
                        continue
                
                if in_code_block:
                    code_lines.append(line)
            
            if code_lines:
                potential_code = '\n'.join(code_lines)
                if "program " in potential_code:
                    return potential_code
        
        # If no code blocks, look for program declaration
        if "program " in content:
            start = content.find("program ")
            if start != -1:
                # Find the end of the program by counting braces
                brace_count = 0
                i = start
                while i < len(content):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            return content[start:i+1]
                    i += 1
        
        return content  # Return as-is if no specific pattern found
    
    async def generate_code(self, requirements: CodeRequirements) -> GeneratedCode:
        """Generate Leo code from requirements"""
        
        system_prompt = self._get_prompt_with_rules()
        
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

Generate the complete Leo program code.
Start the code with: program {requirements.project_name}.aleo {{
End with closing brace.

Return ONLY the Leo code, no explanations or additional text.
"""
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            # Extract content directly
            content = response.content[0].text
            
            # Extract and format the Leo code
            code = self._extract_leo_code_from_text(content)
            formatted_code = self._format_leo_code(code)
            
            return GeneratedCode(
                project_name=requirements.project_name,
                code=formatted_code
            )
                
        except Exception as e:
            c.print(f"[red]Error calling Anthropic API: {e}[/red]")
            raise

    async def fix_compilation_errors(self, 
                                   code: str, 
                                   build_result: BuildResult,
                                   requirements: CodeRequirements) -> GeneratedCode:
        """Fix compilation errors in existing code"""
        
        system_prompt = self._get_prompt_with_rules()
        message = get_error_fix_prompt().format(
            code=code,
            errors=build_result.stderr
        )
        
        message += "\n\nReturn ONLY the corrected Leo code, no explanations or additional text."
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            content = response.content[0].text
            
            # Extract and format the Leo code
            code = self._extract_leo_code_from_text(content)
            formatted_code = self._format_leo_code(code)
            
            return GeneratedCode(
                project_name=requirements.project_name,
                code=formatted_code
            )
                
        except Exception as e:
            c.print(f"[red]Error fixing compilation errors: {e}[/red]")
            raise