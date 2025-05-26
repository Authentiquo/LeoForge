"""
Code Generator Agent - Generates Leo code from normalized requirements
"""
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import CodeRequirements, GeneratedCode, BuildResult
from .prompt import CODE_GENERATOR_SYSTEM_PROMPT


class CodeGeneratorAgent:
    """Agent responsible for generating Leo code from requirements"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-opus-4-20250514"):
        self.system_prompt = CODE_GENERATOR_SYSTEM_PROMPT
        
        # Créer manuellement un AgentOutputSchema avec strict_json_schema=False
        output_schema = AgentOutputSchema(
            output_type=GeneratedCode,
            strict_json_schema=False
        )
        
        self.agent = Agent(
            name="CodeGeneratorAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=output_schema
        )
    
    async def generate_code(self, requirements: CodeRequirements) -> GeneratedCode:
        """Generate Leo code from requirements"""
        
        # Format architecture details
        data_structures = "\n".join([
            f"- {name}: {definition}" 
            for name, definition in requirements.architecture.data_structures.items()
        ])
        
        transitions = "\n".join([
            f"- {name}: {signature}" 
            for name, signature in requirements.architecture.transitions.items()
        ])
        
        features_str = chr(10).join(f"- {feature}" for feature in requirements.features)
        technical_req_str = chr(10).join(f"- {req}" for req in requirements.architecture.technical_requirements)
        security_str = chr(10).join(f"- {sec}" for sec in requirements.architecture.security_considerations)
        
        message = f"""
Generate complete Leo code for the following project:

PROJECT: {requirements.project_name}
TYPE: {requirements.architecture.project_type}
DESCRIPTION: {requirements.description}

FEATURES TO IMPLEMENT:
{features_str}

DATA STRUCTURES:
{data_structures}

TRANSITIONS:
{transitions}

TECHNICAL REQUIREMENTS:
{technical_req_str}

SECURITY CONSIDERATIONS:
{security_str}

Generate the complete Leo program code. Ensure all features are implemented and the code is compilable.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output
    
    async def fix_compilation_errors(self, 
                                   code: str, 
                                   build_result: BuildResult,
                                   requirements: CodeRequirements) -> GeneratedCode:
        
        """Fix compilation errors in existing code"""
        
        message = f"""
Fix the compilation errors in this Leo code:

CURRENT CODE:
```leo
{code}
```

COMPILATION ERRORS:
{build_result.stderr}

ORIGINAL REQUIREMENTS:
- Project: {requirements.project_name}
- Features: {', '.join(requirements.features)}

COMMON ERROR FIXES:
1. "This operation can only be used in an async function" → Move mapping operations to async finalize functions
2. "Mapping::set must be inside an async function block" → Use async transition + finalize pattern
3. "expected ; -- found 'finalize'" → Check syntax: async function finalize_name() with proper braces
4. "expected 'const', 'struct', 'record', 'mapping', '@', 'async', 'function', 'transition', 'inline', 'script', '}}' -- found 'finalize'" → Ensure proper async function syntax

MAPPING FIX PATTERN:
If you see mapping errors, use this pattern:
```leo
async transition function_name(public param: type) -> Future {{{{
    let fut: Future = finalize_function_name(param);
    return fut;
}}}}

async function finalize_function_name(param: type) {{{{
    // Mapping operations here
    Mapping::set(mapping_name, key, value);
}}}}
```

Fix all compilation errors while maintaining the intended functionality.
Generate the corrected Leo code with proper async/finalize patterns.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output 