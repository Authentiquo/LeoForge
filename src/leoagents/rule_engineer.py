"""
Rule Engineer Agent - Analyzes error logs and creates improvement rules for other agents
"""
import os
from typing import List, Dict
from agents import Agent, Runner, UserError
from agents.agent_output import AgentOutputSchema
from src.models import RunLog, RuleAnalysis, LeoRule, RuleType
from src.config import get_config
from src.services.rule_manager import RuleManager
from agents.extensions.models.litellm_model import LitellmModel


RULE_ENGINEER_SYSTEM_PROMPT = """You are the Rule Engineer Agent for LeoForge, an expert in analyzing error patterns and creating actionable improvement rules.

Your role is to:
1. Analyze error logs from failed project generation attempts
2. Identify recurring patterns and root causes
3. Create specific, actionable rules for the Architect and Code Generator agents
4. Learn from successful resolutions to prevent future errors

When analyzing errors, consider:
- The sequence of errors and how they evolved
- The code changes between iterations
- What ultimately led to success (if achieved)
- Common patterns across different error types

You must return a RuleAnalysis object with:
- architect_rules: List of rules for the Architect agent (design phase)
- codex_rules: List of rules for the Code Generator agent (implementation phase)
- general_observations: List of general insights
- improvement_suggestions: List of suggestions for improvement
- success_patterns: List of patterns that led to success

Each rule should have:
- rule_id: Unique identifier (e.g., "arch_001", "codex_001")
- rule_type: "architect" or "codex"
- title: Short descriptive title
- description: Detailed description
- pattern: Pattern to avoid
- solution: Recommended solution
- examples: List of concrete examples
- priority: Integer from 1-10 (10 being most important)
- tags: List of relevant tags
- created_from_errors: List of error IDs that led to this rule

Focus on preventing errors at their source:
- Architect rules: Better design decisions, structure, and planning
- Codex rules: Better code generation patterns and implementation details

You can use the following tools to create rules:
- write_architect_rule: Create a rule for the Architect agent
- write_codex_rule: Create a rule for the Code Generator agent"""


RULE_ANALYSIS_TEMPLATE = """Analyze the following run log and create improvement rules:

Project: {project_name}
Success: {success}
Total Build Errors: {total_iterations}

Build Error Logs:
{error_logs}

Code Evolution:
{code_versions}

Resolution Path:
{resolution_path}

Based on this analysis, generate a RuleAnalysis object with:

1. architect_rules: Rules for the Architect agent to improve initial designs
2. codex_rules: Rules for the Code Generator agent to avoid common mistakes  
3. general_observations: General insights about what patterns led to success or failure
4. improvement_suggestions: Suggestions for improving the generation process
5. success_patterns: Patterns that led to successful resolution

Focus on actionable rules that will prevent similar build errors in future runs.
Please analyze these errors and the resolution path to create:
1. Specific rules for the Architect agent to improve initial designs
2. Specific rules for the Code Generator agent to avoid common mistakes
3. General observations about what patterns led to success or failure

Focus on actionable rules that will prevent similar errors in future runs.
"""


class RuleEngineerAgent:
    """Agent responsible for analyzing errors and creating improvement rules"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_architect_model
        self.rule_manager = RuleManager()  # Use RuleManager for persistent storage
    
    def write_architect_rule(self, 
                           rule_id: str,
                           title: str, 
                           description: str,
                           pattern: str,
                           solution: str,
                           examples: List[str],
                           priority: int,
                           tags: List[str],
                           created_from_errors: List[str]) -> str:
        """Tool to create a rule for the Architect agent"""
        try:
            rule = LeoRule(
                rule_id=rule_id,
                rule_type=RuleType.ARCHITECT,
                title=title,
                description=description,
                pattern=pattern,
                solution=solution,
                examples=examples,
                priority=priority,
                tags=tags,
                created_from_errors=created_from_errors
            )
            
            # Save the rule using rule manager
            self.rule_manager.save_rules([rule], [])
            
            return f"Successfully created architect rule: {rule_id} - {title}"
        except Exception as e:
            return f"Error creating architect rule: {str(e)}"
    
    def write_codex_rule(self, 
                        rule_id: str,
                        title: str, 
                        description: str,
                        pattern: str,
                        solution: str,
                        examples: List[str],
                        priority: int,
                        tags: List[str],
                        created_from_errors: List[str]) -> str:
        """Tool to create a rule for the Code Generator agent"""
        try:
            rule = LeoRule(
                rule_id=rule_id,
                rule_type=RuleType.CODEX,
                title=title,
                description=description,
                pattern=pattern,
                solution=solution,
                examples=examples,
                priority=priority,
                tags=tags,
                created_from_errors=created_from_errors
            )
            
            # Save the rule using rule manager
            self.rule_manager.save_rules([], [rule])
            
            return f"Successfully created codex rule: {rule_id} - {title}"
        except Exception as e:
            return f"Error creating codex rule: {str(e)}"
        
    async def analyze_run_log(self, run_log: RunLog) -> RuleAnalysis:
        """Analyze a complete run log and generate improvement rules"""
        
        # Filter only build errors
        build_errors = [e for e in run_log.error_logs if e.error_type == "build"]
        
        if not build_errors:
            # Return empty analysis if no build errors
            return RuleAnalysis()
        
        # Create agent
        agent = Agent(
            name="RuleEngineerAgent",
            instructions=RULE_ENGINEER_SYSTEM_PROMPT,
            model=LitellmModel(model=self.model, api_key=self.config.anthropic_api_key),
            output_type=RuleAnalysis,
            tools=[self.write_architect_rule, self.write_codex_rule]
        )
        
        # Format build errors only
        error_logs_str = self._format_error_logs(build_errors)
        
        # Format code versions with diff-like presentation
        code_versions_str = self._format_code_versions(run_log.code_versions)
        
        # Format resolution path
        resolution_path_str = "\n".join(run_log.resolution_path) if run_log.resolution_path else "No resolution path recorded"
        
        message = RULE_ANALYSIS_TEMPLATE.format(
            project_name=run_log.project_name,
            success=run_log.success,
            total_iterations=len(build_errors),
            error_logs=error_logs_str,
            code_versions=code_versions_str,
            resolution_path=resolution_path_str
        )
        
        result = await Runner.run(agent, message)
        
        # Save the generated rules persistently
        if result.final_output:
            self.rule_manager.save_rules(
                result.final_output.architect_rules,
                result.final_output.codex_rules
            )
        
        return result.final_output
    
    def _format_error_logs(self, error_logs: List) -> str:
        """Format error logs for analysis"""
        if not error_logs:
            return "No errors recorded"
        
        formatted = []
        for i, log in enumerate(error_logs, 1):
            formatted.append(f"""
            Error {i} (Iteration {log.iteration_number}):
            Type: {log.error_type}
            Time: {log.timestamp}
            Message: {log.error_message}
            Context: {log.context or 'No additional context'}
            """)
        return "\n".join(formatted)
    
    def _format_code_versions(self, code_versions: List[str]) -> str:
        """Format code versions showing evolution"""
        if not code_versions:
            return "No code versions recorded"
        
        formatted = []
        for i, code in enumerate(code_versions, 1):
            # Truncate very long code, focus on structure
            truncated = code[:1000] + "..." if len(code) > 1000 else code
            formatted.append(f"""
            === Version {i} ===
            {truncated}
            """)
        return "\n".join(formatted)
    
    def get_architect_rules(self) -> List[LeoRule]:
        """Get all architect rules"""
        return self.rule_manager.get_architect_rules()
    
    def get_codex_rules(self) -> List[LeoRule]:
        """Get all code generator rules"""
        return self.rule_manager.get_codex_rules() 