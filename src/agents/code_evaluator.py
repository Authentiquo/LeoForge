"""
Code Evaluator Agent - Evaluates generated Leo code for completeness and quality
"""
from agents import Agent, Runner
from agents.agent_output import AgentOutputSchema
from src.models import GeneratedCode, CodeRequirements, EvaluationResult


class CodeEvaluatorAgent:
    """Agent responsible for evaluating generated Leo code"""
    
    def __init__(self, model: str = "litellm/anthropic/claude-3-5-sonnet-20241022"):
        self.system_prompt = """
You are an expert Leo code reviewer and security auditor.

Your role is to evaluate generated Leo code for:
1. Completeness - Are all required features implemented?
2. Correctness - Is the logic sound and bug-free?
3. Security - Are there vulnerabilities or risks?
4. Optimization - Can the code be more efficient?
5. Best Practices - Does it follow Leo/Aleo conventions?

EVALUATION CRITERIA:
- Feature Coverage: Check if all requested features are implemented
- Logic Errors: Identify any logical flaws or bugs
- Security Issues: Look for vulnerabilities (overflow, access control, etc.)
- Gas Efficiency: Suggest optimizations for lower execution cost
- Code Quality: Readability, maintainability, documentation
- Edge Cases: Check if edge cases are handled

SCORING GUIDELINES:
- 90-100: Production ready, minor improvements only
- 70-89: Good quality, some improvements needed
- 50-69: Functional but needs significant improvements
- 0-49: Major issues, needs substantial rework

Be thorough but constructive. Focus on actionable improvements.
"""
        
        self.agent = Agent(
            name="CodeEvaluatorAgent",
            instructions=self.system_prompt,
            model=model,
            output_type=AgentOutputSchema(EvaluationResult, strict_json_schema=False)
        )
    
    async def evaluate_code(self, 
                          generated_code: GeneratedCode,
                          requirements: CodeRequirements) -> EvaluationResult:
        """Evaluate generated code against requirements"""
        
        message = f"""
Evaluate this Leo code against the requirements:

REQUIREMENTS:
- Project: {requirements.project_name}
- Type: {requirements.architecture.project_type}
- Features: {', '.join(requirements.features)}
- Technical Requirements: {', '.join(requirements.architecture.technical_requirements)}
- Security Considerations: {', '.join(requirements.architecture.security_considerations)}

CODE TO EVALUATE:
```leo
{generated_code.code}
```

Perform a comprehensive evaluation covering:
1. Feature completeness
2. Logic correctness
3. Security vulnerabilities
4. Optimization opportunities
5. Code quality

Provide specific, actionable feedback and a quality score.
"""
        
        result = await Runner.run(self.agent, message)
        return result.final_output 