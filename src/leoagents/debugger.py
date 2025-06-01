"""
Leo Debugger Agent - Interactive debugging and fixing of Leo code
"""
import asyncio
import subprocess
import re
from typing import Optional, List, Dict, Tuple
from agents import Agent, Runner, trace, Tool
from agents.agent_output import AgentOutputSchema
from agents.extensions.models.litellm_model import LitellmModel
from src.models import (
    DebuggerState, DebugCommand, DebugResult, DebugSession, 
    DebugAnalysis, DebugContext, Breakpoint, BreakpointType,
    GeneratedCode
)
from src.config import get_config
from rich import console
import uuid

c = console.Console()


class LeoDebuggerTool:
    """Tool to interact with Leo debugger"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.process = None
        self.current_session: Optional[DebugSession] = None
        
    async def start_debugger(self, program_name: str) -> bool:
        """Start Leo debugger for a program"""
        try:
            # Start leo debug in interactive mode
            self.process = await asyncio.create_subprocess_exec(
                'leo', 'debug',
                cwd=self.workspace_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for prompt
            await asyncio.sleep(0.5)
            
            # Set program context
            await self.send_command(f"#set_program {program_name}")
            return True
            
        except Exception as e:
            c.print(f"[red]Failed to start debugger: {e}[/red]")
            return False
    
    async def send_command(self, command: str) -> str:
        """Send command to debugger and get response"""
        if not self.process:
            return "Debugger not started"
            
        try:
            # Send command
            self.process.stdin.write(f"{command}\n".encode())
            await self.process.stdin.drain()
            
            # Read response with timeout
            response = ""
            while True:
                try:
                    line = await asyncio.wait_for(
                        self.process.stdout.readline(), 
                        timeout=2.0
                    )
                    if not line:
                        break
                    decoded = line.decode()
                    response += decoded
                    if "✔ Command?" in decoded or "Result:" in decoded:
                        break
                except asyncio.TimeoutError:
                    break
                    
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def stop_debugger(self):
        """Stop the debugger process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.process = None
    
    def parse_debug_output(self, output: str) -> DebugResult:
        """Parse debugger output into structured result"""
        success = "Error:" not in output and "Failed" not in output
        
        # Extract current line if stepping
        current_line = None
        line_match = re.search(r'Line (\d+):', output)
        if line_match:
            current_line = int(line_match.group(1))
        
        # Extract variable values
        variables = {}
        var_matches = re.findall(r'(\w+):\s*(.+?)(?:\n|$)', output)
        for var, val in var_matches:
            variables[var] = val
        
        context = DebugContext(
            current_line=current_line or 0,
            variables=variables
        ) if current_line else None
        
        return DebugResult(
            success=success,
            output=output,
            context=context,
            error=output if not success else None
        )


class DebuggerAgent:
    """Agent responsible for debugging and fixing Leo code"""
    
    def __init__(self, model: str = None):
        self.config = get_config()
        self.model = model or self.config.default_debugger_model
        self.debugger_tool = None
        
    def _create_debug_tools(self) -> List[Tool]:
        """Create tools for the debugging agent"""
        
        async def step_through_code(line_count: int = 1) -> DebugResult:
            """Step through code line by line"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            results = []
            for _ in range(line_count):
                output = await self.debugger_tool.send_command("#step")
                results.append(output)
            
            return self.debugger_tool.parse_debug_output("\n".join(results))
        
        async def step_over() -> DebugResult:
            """Step over current statement"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command("#over")
            return self.debugger_tool.parse_debug_output(output)
        
        async def step_into_function(function_call: str) -> DebugResult:
            """Step into a function call"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command(f"#into {function_call}")
            return self.debugger_tool.parse_debug_output(output)
        
        async def set_breakpoint(line_number: int) -> DebugResult:
            """Set a breakpoint at specific line"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            program = self.debugger_tool.current_session.program_name if self.debugger_tool.current_session else "main"
            output = await self.debugger_tool.send_command(f"#break {program} {line_number}")
            return self.debugger_tool.parse_debug_output(output)
        
        async def run_until_breakpoint() -> DebugResult:
            """Run until next breakpoint or error"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command("#run")
            return self.debugger_tool.parse_debug_output(output)
        
        async def evaluate_expression(expression: str) -> DebugResult:
            """Evaluate an expression in current context"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command(expression)
            return self.debugger_tool.parse_debug_output(output)
        
        async def watch_variable(variable_name: str) -> DebugResult:
            """Watch a variable's value during execution"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command(f"#watch {variable_name}")
            return self.debugger_tool.parse_debug_output(output)
        
        async def restore_state() -> DebugResult:
            """Restore to last valid state"""
            if not self.debugger_tool:
                return DebugResult(success=False, output="Debugger not initialized")
                
            output = await self.debugger_tool.send_command("#restore")
            return self.debugger_tool.parse_debug_output(output)
        
        return [
            Tool(step_through_code),
            Tool(step_over),
            Tool(step_into_function),
            Tool(set_breakpoint),
            Tool(run_until_breakpoint),
            Tool(evaluate_expression),
            Tool(watch_variable),
            Tool(restore_state)
        ]
    
    async def debug_code(self, 
                        code: str, 
                        error_message: str,
                        workspace_path: str,
                        program_name: str = "main") -> DebugAnalysis:
        """Debug Leo code and identify the root cause of errors"""
        
        with trace("debug_code"):
            # Initialize debugger tool
            self.debugger_tool = LeoDebuggerTool(workspace_path)
            
            # Create debug session
            session = DebugSession(
                session_id=str(uuid.uuid4()),
                program_name=program_name,
                code=code
            )
            self.debugger_tool.current_session = session
            
            # Start debugger
            await self.debugger_tool.start_debugger(program_name)
            
            # Create agent with tools
            agent = Agent(
                name="LeoDebuggerAgent",
                instructions=self._get_debug_prompt(),
                model=LitellmModel(model=self.model, api_key=self.config.openai_api_key),
                tools=self._create_debug_tools(),
                output_type=DebugAnalysis
            )
            
            message = f"""
            Debug the following Leo code that is producing an error:
            
            ERROR MESSAGE:
            {error_message}
            
            LEO CODE:
            ```leo
            {code}
            ```
            
            Please:
            1. Use the debugging tools to step through the code
            2. Identify the exact line where the error occurs
            3. Determine the root cause of the error
            4. Suggest a fix for the error
            5. If possible, provide the corrected code
            
            Focus on finding the EXACT location and cause of the error.
            """
            
            try:
                result = await Runner.run(agent, message)
                return result.final_output
            finally:
                # Clean up debugger
                await self.debugger_tool.stop_debugger()
    
    async def fix_code_interactive(self,
                                  code: str,
                                  debug_analysis: DebugAnalysis) -> GeneratedCode:
        """Fix code based on debug analysis"""
        
        with trace("fix_code_interactive"):
            agent = Agent(
                name="LeoCodeFixerAgent", 
                instructions=self._get_fix_prompt(),
                model=LitellmModel(model=self.model, api_key=self.config.openai_api_key),
                output_type=GeneratedCode
            )
            
            message = f"""
            Fix the following Leo code based on the debug analysis:
            
            ORIGINAL CODE:
            ```leo
            {code}
            ```
            
            DEBUG ANALYSIS:
            - Error Location: Line {debug_analysis.error_location}
            - Error Type: {debug_analysis.error_type}
            - Root Cause: {debug_analysis.root_cause}
            - Suggested Fix: {debug_analysis.suggested_fix}
            
            Generate the complete FIXED Leo code that resolves this error.
            Make sure to maintain all existing functionality while fixing the error.
            """
            
            result = await Runner.run(agent, message)
            return result.final_output
    
    def _get_debug_prompt(self) -> str:
        """Get prompt for debugging agent"""
        return """You are an expert Leo debugger. Your role is to:

1. Use the Leo debugger tools to systematically step through code
2. Identify the exact location where errors occur
3. Analyze variable states and execution flow
4. Determine root causes of compilation or runtime errors
5. Provide clear, actionable fixes

AVAILABLE TOOLS:
- step_through_code(line_count): Step through N lines
- step_over(): Step over current statement
- step_into_function(function_call): Step into a function
- set_breakpoint(line_number): Set breakpoint at line
- run_until_breakpoint(): Run until breakpoint/error
- evaluate_expression(expression): Evaluate Leo expression
- watch_variable(variable_name): Watch variable values
- restore_state(): Restore to last valid state

DEBUGGING STRATEGY:
1. First, identify the general area of the error from the message
2. Set breakpoints around suspicious areas
3. Step through code line by line near the error
4. Watch relevant variables
5. Evaluate expressions to test hypotheses
6. Identify the exact line and root cause

Be systematic and thorough. Test your hypotheses with the debugger."""
    
    def _get_fix_prompt(self) -> str:
        """Get prompt for code fixing"""
        return """You are an expert Leo code fixer. Based on debug analysis:

1. Apply the exact fix needed to resolve the error
2. Ensure the fix doesn't break other functionality
3. Maintain Leo syntax and best practices
4. Keep all original features intact
5. Only modify what's necessary to fix the error

Generate the complete, corrected Leo code.""" 