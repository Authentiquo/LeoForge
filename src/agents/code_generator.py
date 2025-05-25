"""
Code Generator Agent - Generates Leo code from normalized requirements
"""
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import CodeRequirements, GeneratedCode, BuildResult


class CodeGeneratorAgent:
    """Agent responsible for generating Leo code from requirements"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-3-5-sonnet-20241022"):
        self.system_prompt = """
You are an expert Leo code generator for the Aleo blockchain.

Your role is to generate complete, compilable Leo code based on detailed requirements.

CRITICAL LEO SYNTAX RULES:
1. Program declaration: program project_name.aleo { ... }
2. Records MUST have owner field: record Name { owner: address, field: type }
3. Mappings can ONLY be used in async finalize functions
4. Use async transition + async function finalize pattern for mapping operations
5. Transitions: transition name(input: type) -> output_type { ... }
6. Async transitions: async transition name() -> Future { ... }
7. Finalize functions: async function finalize_name() { ... }
8. Mapping operations: Mapping::get(), Mapping::set(), Mapping::get_or_use()
9. Context access: self.caller, self.signer, block.height (in finalize only)
10. Types: u8-u128, i8-i128, address, bool, field, scalar, group, [T; N]

MAPPING USAGE PATTERN (CRITICAL):
```leo
// Declare mapping at program level
mapping balances: address => u64;

// Use async transition for mapping operations
async transition transfer_public(to: address, amount: u64) -> Future {
    let fut: Future = finalize_transfer_public(self.caller, to, amount);
    return fut;
}

// Implement logic in finalize function
async function finalize_transfer_public(from: address, to: address, amount: u64) {
    let from_balance: u64 = Mapping::get(balances, from);
    assert(from_balance >= amount);
    let to_balance: u64 = Mapping::get_or_use(balances, to, 0u64);
    Mapping::set(balances, from, from_balance - amount);
    Mapping::set(balances, to, to_balance + amount);
}
```

RECORD PATTERN:
```leo
record Token {
    owner: address,  // REQUIRED
    amount: u64,
}

transition transfer_private(token: Token, to: address, amount: u64) -> (Token, Token) {
    assert_eq(token.owner, self.caller);
    assert(amount <= token.amount);
    
    let recipient_token: Token = Token {
        owner: to,
        amount: amount,
    };
    
    let sender_token: Token = Token {
        owner: self.caller,
        amount: token.amount - amount,
    };
    
    return (recipient_token, sender_token);
}
```

VALIDATION PATTERNS:
- assert(amount > 0u64);
- assert_eq(token.owner, self.caller);
- assert(balance >= amount); // Prevent underflow
- assert(balance + amount >= balance); // Prevent overflow

BEST PRACTICES:
- Use clear, descriptive names
- Add comments for complex logic
- Always validate inputs with assertions
- Use appropriate visibility (private/public)
- Handle edge cases and overflows
- Use async transitions for mapping operations
- Never use mappings directly in transitions

CODE STRUCTURE:
1. Program declaration
2. Constants (if needed)
3. Struct definitions
4. Record definitions
5. Mapping declarations
6. Inline functions (if needed)
7. Transition implementations
8. Async transitions
9. Finalize functions

Generate ONLY valid, compilable Leo code. Do not include explanations outside code comments.
"""
        
        self.agent = Agent(
            name="CodeGeneratorAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=AgentOutputSchema(GeneratedCode, strict_json_schema=False)
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
        
        message = f"""
Generate complete Leo code for the following project:

PROJECT: {requirements.project_name}
TYPE: {requirements.architecture.project_type}
DESCRIPTION: {requirements.description}

FEATURES TO IMPLEMENT:
{chr(10).join(f"- {feature}" for feature in requirements.features)}

DATA STRUCTURES:
{data_structures}

TRANSITIONS:
{transitions}

TECHNICAL REQUIREMENTS:
{chr(10).join(f"- {req}" for req in requirements.architecture.technical_requirements)}

SECURITY CONSIDERATIONS:
{chr(10).join(f"- {sec}" for sec in requirements.architecture.security_considerations)}

Generate the complete Leo program code. Ensure all features are implemented and the code is compilable.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output
    
    async def fix_compilation_errors(self, 
                                   code: str, 
                                   build_result: BuildResult,
                                   requirements: CodeRequirements) -> GeneratedCode:
        """Fix compilation errors in existing code"""
        
        error_fixes = """
COMMON ERROR FIXES:
1. "This operation can only be used in an async function" → Move mapping operations to async finalize functions
2. "Mapping::set must be inside an async function block" → Use async transition + finalize pattern
3. "expected ; -- found 'finalize'" → Check syntax: async function finalize_name() with proper braces
4. "expected 'const', 'struct', 'record', 'mapping', '@', 'async', 'function', 'transition', 'inline', 'script', '}' -- found 'finalize'" → Ensure proper async function syntax

MAPPING FIX PATTERN:
If you see mapping errors, use this pattern:
```leo
async transition function_name(public param: type) -> Future {
    let fut: Future = finalize_function_name(param);
    return fut;
}

async function finalize_function_name(param: type) {
    // Mapping operations here
    Mapping::set(mapping_name, key, value);
}
```
"""
        
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

{error_fixes}

Fix all compilation errors while maintaining the intended functionality.
Generate the corrected Leo code with proper async/finalize patterns.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output 