import os
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from agents import Agent, Runner, FunctionTool

from ..tools.leo_tools import save_leo_code
from ..tools.agent_tools import (
    create_project_tool_function,
    save_code_tool_function,
    build_project_tool_function,
    verify_code_tool_function
)

console = Console()

class LeoCodeGenerator:
    def __init__(self):
        self.system_prompt = self._load_system_prompt()
        # Create an agent with function tools
        self.agent = Agent(
            name="LeoExpert",
            instructions=self.system_prompt,
            model="gpt-4-turbo",
            tools=[
                verify_code_tool_function
            ]
        )
        
    def _load_system_prompt(self):
        """Load the system prompt for Leo code generation from file."""
        prompt_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "system_prompt.md")
        try:
            with open(prompt_file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            console.print(f"[bold red]System prompt file not found: {prompt_file}[/bold red]")
            # Return the default prompt
            return """
            You are an expert in the Leo programming language for the Aleo blockchain.
            
            Guidelines for Leo code generation:
            1. Leo is a statically-typed language with syntax similar to Rust but with key differences
            2. Program structure includes a program declaration, imports, and function definitions
            3. Types in Leo include u8, u16, u32, u64, i8, i16, i32, i64, field, group, address, bool, and arrays
            4. Records are defined with the 'record' keyword and can have public and private fields
            5. Functions can be public or private using the 'function' keyword
            6. Use the '@program' directive to define the program ID
            7. Maps are defined using the 'mapping' keyword
            8. For importing other programs, use the 'import' statement
            """
    
    def generate_code(self, project_name, user_requirements):
        """Generate Leo code based on user requirements."""
        console.print(Panel.fit("[bold blue]Generating Leo code...[/bold blue]"))
        
        with Progress() as progress:
            task = progress.add_task("[green]Running code generation...", total=100)
            
            # First, prepare the user prompt
            user_prompt = f"""
            Generate a complete Leo program for the following project: {project_name}
            
            Requirements:
            {user_requirements}
            
            Provide the complete Leo code with proper syntax.
            Always include the @program directive and at least one function.
            """
            
            progress.update(task, advance=30)
            
            # Generate code using OpenAI Agents SDK
            result = Runner.run_sync(self.agent, user_prompt)
            
            progress.update(task, advance=50)
            
            # Extract code from response
            generated_code = result.final_output.strip()
            
            # Remove markdown code blocks if present
            if generated_code.startswith("```leo"):
                generated_code = generated_code.split("```leo")[1]
            if generated_code.startswith("```"):
                generated_code = generated_code.split("```")[1]
            if generated_code.endswith("```"):
                generated_code = generated_code.rsplit("```", 1)[0]
                
            generated_code = generated_code.strip()
            
            # Use the verify_code_tool to check the code
            if result.tool_results:
                # If the agent used the verification tool, show the results
                for tool_result in result.tool_results:
                    if tool_result.tool_name == "verify_leo_code":
                        verification_result = tool_result.output
                        if not verification_result.is_valid:
                            console.print("[bold yellow]Code verification found issues:[/bold yellow]")
                            for issue in verification_result.issues:
                                console.print(f"[yellow]- {issue}[/yellow]")
                            for suggestion in verification_result.suggestions:
                                console.print(f"[green]- Suggestion: {suggestion}[/green]")
            
            progress.update(task, advance=20)
            
            # Save the generated code to a file
            program_file_path = f"temp_{project_name}/src/main.leo"
            save_leo_code(project_name, program_file_path, generated_code)
            
            return generated_code
    
    def evaluate_code(self, leo_code):
        """Evaluate the quality of the generated Leo code."""
        evaluation_prompt = f"""
        Evaluate the following Leo code on a scale of 1-10 for:
        1. Correctness (Does it follow Leo syntax correctly?)
        2. Completeness (Does it implement all necessary features?)
        3. Efficiency (Is the code efficient?)
        4. Readability (Is the code easy to read and understand?)
        
        Leo code to evaluate:
        {leo_code}
        
        Provide a score for each category and brief justification.
        """
        
        # Use the agent to evaluate the code
        result = Runner.run_sync(self.agent, evaluation_prompt)
        
        evaluation = result.final_output
        console.print(Panel.fit(f"[bold yellow]Code Evaluation:[/bold yellow]\n{evaluation}", title="Evaluation"))
        
        return evaluation 