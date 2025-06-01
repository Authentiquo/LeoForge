#!/usr/bin/env python3
"""
Leo Debugger Agent
An automated agent for debugging Leo programs on Aleo blockchain
"""

import subprocess
import re
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DebugCommand(Enum):
    """Leo debugger commands"""
    HELP = "#help"
    INTO = "#i"
    STEP = "#s"
    OVER = "#o"
    RUN = "#r"
    BREAK = "#break"
    RESTORE = "#restore"
    SET_PROGRAM = "#set_program"
    WATCH = "#watch"
    PRINT = "#p"
    

@dataclass
class DebugResult:
    """Result from a debug command"""
    success: bool
    output: str
    error: Optional[str] = None
    value: Optional[Any] = None


class LeoDebuggerAgent:
    """Agent for interacting with Leo debugger"""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.process = None
        self.current_program = None
        self.breakpoints = []
        self.watch_expressions = []
        
    def start_debugger(self, tui_mode: bool = False) -> DebugResult:
        """Start the Leo debugger"""
        try:
            cmd = ["leo", "debug"]
            if tui_mode:
                cmd.append("--tui")
                
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_path
            )
            
            # Wait for initial prompt
            output = self._read_until_prompt()
            return DebugResult(success=True, output=output)
            
        except Exception as e:
            return DebugResult(success=False, output="", error=str(e))
    
    def stop_debugger(self) -> None:
        """Stop the debugger process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
            
    def execute_command(self, command: str) -> DebugResult:
        """Execute a command in the debugger"""
        if not self.process:
            return DebugResult(success=False, output="", error="Debugger not started")
            
        try:
            # Send command
            self.process.stdin.write(f"{command}\n")
            self.process.stdin.flush()
            
            # Read response
            output = self._read_until_prompt()
            
            # Parse result if it's an expression
            value = self._parse_result(output)
            
            return DebugResult(success=True, output=output, value=value)
            
        except Exception as e:
            return DebugResult(success=False, output="", error=str(e))
    
    def set_program(self, program_name: str) -> DebugResult:
        """Set the current program context"""
        self.current_program = program_name
        return self.execute_command(f"{DebugCommand.SET_PROGRAM.value} {program_name}")
    
    def step_into(self, expression: str) -> DebugResult:
        """Step into a function or expression"""
        return self.execute_command(f"{DebugCommand.INTO.value} {expression}")
    
    def step_over(self) -> DebugResult:
        """Step over current expression"""
        return self.execute_command(DebugCommand.OVER.value)
    
    def step(self) -> DebugResult:
        """Take a single step"""
        return self.execute_command(DebugCommand.STEP.value)
    
    def run(self) -> DebugResult:
        """Run until completion"""
        return self.execute_command(DebugCommand.RUN.value)
    
    def set_breakpoint(self, program: str, line_number: int) -> DebugResult:
        """Set a breakpoint"""
        self.breakpoints.append((program, line_number))
        return self.execute_command(f"{DebugCommand.BREAK.value} {program} {line_number}")
    
    def restore(self) -> DebugResult:
        """Restore to last stable state"""
        return self.execute_command(DebugCommand.RESTORE.value)
    
    def watch(self, expression: str) -> DebugResult:
        """Add a watch expression"""
        self.watch_expressions.append(expression)
        return self.execute_command(f"{DebugCommand.WATCH.value} {expression}")
    
    def evaluate(self, expression: str) -> DebugResult:
        """Evaluate a Leo expression"""
        return self.execute_command(expression)
    
    def print_register(self, register_number: int) -> DebugResult:
        """Print AVM register value"""
        return self.execute_command(f"{DebugCommand.PRINT.value} {register_number}")
    
    def create_struct(self, struct_type: str, **fields) -> DebugResult:
        """Create a struct with given fields"""
        field_str = ", ".join([f"{k}: {v}" for k, v in fields.items()])
        expr = f"{struct_type} {{ {field_str} }}"
        return self.evaluate(expr)
    
    def call_function(self, function_name: str, *args) -> DebugResult:
        """Call a Leo function with arguments"""
        args_str = ", ".join(str(arg) for arg in args)
        expr = f"{function_name}({args_str})"
        return self.evaluate(expr)
    
    def declare_variable(self, name: str, var_type: str, value: str) -> DebugResult:
        """Declare a variable"""
        expr = f"let {name}: {var_type} = {value};"
        return self.evaluate(expr)
    
    def access_mapping(self, mapping_name: str, key: str) -> DebugResult:
        """Access a mapping value"""
        expr = f"{mapping_name}.get({key})"
        return self.evaluate(expr)
    
    def print_mapping(self, mapping_name: str) -> DebugResult:
        """Print entire mapping using CheatCode"""
        expr = f"CheatCode::print_mapping({mapping_name})"
        return self.evaluate(expr)
    
    def set_block_height(self, height: int) -> DebugResult:
        """Set block height using CheatCode"""
        expr = f"CheatCode::set_block_height({height}u32)"
        return self.evaluate(expr)
    
    def await_future(self, future_var: str) -> DebugResult:
        """Await a future"""
        expr = f"{future_var}.await()"
        return self.evaluate(expr)
    
    def _read_until_prompt(self) -> str:
        """Read output until we see the prompt"""
        output = []
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            output.append(line)
            if "✔ Command?" in line or "Result:" in line:
                break
        return "".join(output)
    
    def _parse_result(self, output: str) -> Optional[Any]:
        """Parse the result value from output"""
        match = re.search(r"Result: (.+)", output)
        if match:
            result_str = match.group(1).strip()
            # Try to parse different types
            if result_str.startswith("Point {"):
                # Parse Point struct
                return self._parse_struct(result_str)
            elif result_str.endswith(("u8", "u16", "u32", "u64", "u128")):
                # Parse unsigned integer
                return int(result_str[:-2] if result_str[-2].isdigit() else result_str[:-3])
            elif result_str == "()":
                return None
            else:
                return result_str
        return None
    
    def _parse_struct(self, struct_str: str) -> Dict[str, Any]:
        """Parse a struct string into a dictionary"""
        # Simple parser for struct format
        # This is a basic implementation and might need enhancement
        struct_dict = {}
        # Extract fields between {}
        match = re.search(r"{(.+)}", struct_str)
        if match:
            fields_str = match.group(1)
            # Split by comma and parse each field
            fields = fields_str.split(",")
            for field in fields:
                if ":" in field:
                    key, value = field.split(":", 1)
                    struct_dict[key.strip()] = value.strip()
        return struct_dict


class LeoDebugSession:
    """Context manager for Leo debug sessions"""
    
    def __init__(self, project_path: str, program_name: Optional[str] = None):
        self.agent = LeoDebuggerAgent(project_path)
        self.program_name = program_name
        
    def __enter__(self):
        self.agent.start_debugger()
        if self.program_name:
            self.agent.set_program(self.program_name)
        return self.agent
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.agent.stop_debugger()


# Example usage functions
def debug_sqrt_function(project_path: str):
    """Example: Debug the sqrt_bitwise function"""
    with LeoDebugSession(project_path, "point_math") as debugger:
        # Test sqrt function with different inputs
        test_values = [0, 4, 9, 16, 25]
        
        for value in test_values:
            result = debugger.step_into(f"sqrt_bitwise({value}u32)")
            print(f"Stepping into sqrt_bitwise({value})")
            
            result = debugger.step_over()
            print(f"Result: {result.value}")
            print("-" * 40)


def debug_point_operations(project_path: str):
    """Example: Debug Point struct operations"""
    with LeoDebugSession(project_path, "point_math") as debugger:
        # Create points
        debugger.declare_variable("p1", "Point", "create_point(1u32, 2u32)")
        debugger.declare_variable("p2", "Point", "create_point(3u32, 4u32)")
        
        # Calculate distance
        result = debugger.declare_variable("d", "u32", "distance(p1, p2)")
        print(f"Distance: {result.value}")
        
        # Add points
        result = debugger.declare_variable("sum", "Point", "add_points(p1, p2)")
        print(f"Sum: {result.value}")


def debug_with_breakpoints(project_path: str):
    """Example: Debug with breakpoints and watches"""
    with LeoDebugSession(project_path, "access_control") as debugger:
        # Set breakpoint
        debugger.set_breakpoint("access_control", 10)
        
        # Add watch expression
        debugger.watch("self.caller")
        
        # Execute function
        result = debugger.call_function("set_timelock", "self.caller", "1u32")
        print(f"Function result: {result.output}")


if __name__ == "__main__":
    # Example usage
    project_path = "/path/to/leo/project"
    
    print("Leo Debugger Agent Examples")
    print("=" * 50)
    
    # Uncomment to run examples
    # debug_sqrt_function(project_path)
    # debug_point_operations(project_path)
    # debug_with_breakpoints(project_path) 