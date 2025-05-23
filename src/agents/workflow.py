import os
import json
from agents import Agent, Runner, Handoff
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from ..tools.leo_tools import create_leo_project, build_leo_project, verify_private_key
from ..utils.composition import create_composite_project, add_import_to_code
from .leo_agent import LeoCodeGenerator
from ..tools.agent_tools import (
    create_project_tool_function,
    save_code_tool_function,
    build_project_tool_function,
    verify_code_tool_function
)

console = Console()

class LeoWorkflow:
    def __init__(self):
        self.leo_generator = LeoCodeGenerator()
        
        # Create specialized agents for different tasks
        self.architect_agent = Agent(
            name="LeoArchitect", 
            instructions="""
            You are an expert Leo architect who analyzes requirements and designs optimal component structures.
            You excel at breaking down complex blockchain applications into well-structured components.
            """,
            model="gpt-4-turbo"
        )
        
        self.builder_agent = Agent(
            name="LeoBuilder",
            instructions="""
            You are an expert Leo builder who specializes in setting up and compiling Leo projects.
            You manage project creation, dependencies, and ensuring successful compilation.
            """,
            model="gpt-4-turbo",
            tools=[
                create_project_tool_function,
                build_project_tool_function
            ]
        )
        
        self.evaluator_agent = Agent(
            name="LeoEvaluator",
            instructions="""
            You are an expert in Leo code evaluation who thoroughly analyzes code for correctness,
            efficiency, and adherence to best practices. You provide detailed technical feedback to improve code quality.
            """,
            model="gpt-4-turbo",
            tools=[
                verify_code_tool_function
            ]
        )
        
        # Set up handoffs
        self.architect_agent.add_handoff(Handoff(
            to_agent=self.leo_generator.agent,
            description="Generate Leo code for a component"
        ))
        
        self.leo_generator.agent.add_handoff(Handoff(
            to_agent=self.evaluator_agent,
            description="Evaluate generated Leo code"
        ))
        
        self.evaluator_agent.add_handoff(Handoff(
            to_agent=self.builder_agent,
            description="Build a Leo project"
        ))
        
    def execute_workflow(self, project_name, user_input):
        """Execute the complete Leo code generation workflow."""
        console.print(Panel.fit(
            "[bold blue]Starting Leo Code Generation Workflow[/bold blue]",
            subtitle=f"Project: {project_name}"
        ))
        
        # Step 1: Analyze user input to identify components
        components = self._analyze_components(project_name, user_input)
        
        # Step 2: Create Leo projects for each component
        project_paths = self._create_projects(components)
        if not project_paths:
            console.print("[bold red]Failed to create Leo projects. Aborting workflow.[/bold red]")
            return False
        
        # Step 3: Get private key from user (with validation)
        private_key = self._get_private_key()
        if not private_key:
            console.print("[bold yellow]Continuing without private key. Some features may be limited.[/bold yellow]")
        
        # Step 4: Generate Leo code for each component
        generated_code = self._generate_code(project_paths, components)
        if not generated_code:
            console.print("[bold red]Failed to generate Leo code. Aborting workflow.[/bold red]")
            return False
        
        # Step 5: Evaluate generated code
        self._evaluate_code(generated_code)
        
        # Step 6: Build the projects
        build_success = self._build_projects(project_paths)
        if not build_success:
            console.print("[bold red]Failed to build Leo projects.[/bold red]")
            return False
        
        console.print(Panel.fit(
            "[bold green]Leo Code Generation Workflow Completed Successfully[/bold green]",
            subtitle=f"Project: {project_name}"
        ))
        
        return True
    
    def _analyze_components(self, project_name, user_input):
        """Analyze user input to identify components for the Leo program."""
        console.print("[bold]Analyzing requirements to identify components...[/bold]")
        
        analysis_prompt = f"""
        Analyze the following requirements for a Leo program:
        
        {user_input}
        
        Determine if this should be implemented as a single program or multiple composable programs.
        If multiple programs are needed, identify each component and its purpose.
        
        Format your response as a JSON object with the following structure:
        {{
            "approach": "single" or "multiple",
            "components": [
                {{
                    "name": "component_name",
                    "purpose": "brief description",
                    "depends_on": ["other_component_names"] (or empty if no dependencies)
                }}
            ]
        }}
        """
        
        # Use the architect agent to analyze components
        result = Runner.run_sync(
            self.architect_agent, 
            analysis_prompt, 
            model_kwargs={"response_format": {"type": "json_object"}, "temperature": 0.2}
        )
        
        try:
            components = json.loads(result.final_output)
            console.print(f"[green]Identified approach: {components['approach']}[/green]")
            
            for comp in components['components']:
                dependencies = ", ".join(comp.get('depends_on', [])) or "None"
                console.print(f"[green]Component: {comp['name']} (Dependencies: {dependencies})[/green]")
                console.print(f"[green]Purpose: {comp['purpose']}[/green]")
            
            return components
        
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[bold red]Error analyzing components: {str(e)}[/bold red]")
            # Fallback to single component
            return {
                "approach": "single",
                "components": [
                    {
                        "name": project_name,
                        "purpose": "Main program",
                        "depends_on": []
                    }
                ]
            }
    
    def _create_projects(self, components):
        """Create Leo projects for each component using the builder agent."""
        console.print("[bold]Creating Leo projects...[/bold]")
        
        project_paths = {}
        
        if components["approach"] == "single":
            # Single project approach
            comp = components["components"][0]
            
            create_prompt = f"""
            Create a new Leo project for component: {comp['name']}
            Purpose: {comp['purpose']}
            Type: Single component
            
            Use the create_leo_project tool to create this project.
            """
            
            result = Runner.run_sync(self.builder_agent, create_prompt)
            
            # Check if the agent used the create_project_tool
            for tool_result in result.tool_results:
                if tool_result.tool_name == "create_leo_project":
                    if tool_result.output["success"]:
                        project_paths[comp['name']] = tool_result.output["project_path"]
        else:
            # Multiple project approach with dependencies
            # Sort components based on dependencies
            sorted_components = self._sort_components_by_dependencies(components["components"])
            
            # Create projects in dependency order
            for comp in sorted_components:
                dependencies = comp.get('depends_on', [])
                dep_string = ", ".join(dependencies) if dependencies else "None"
                
                create_prompt = f"""
                Create a new Leo project for component: {comp['name']}
                Purpose: {comp['purpose']}
                Dependencies: {dep_string}
                Type: {'Composite' if dependencies else 'Standard'} component
                
                Use the create_leo_project tool to create this project.
                """
                
                result = Runner.run_sync(self.builder_agent, create_prompt)
                
                # Check if the agent used the create_project_tool
                for tool_result in result.tool_results:
                    if tool_result.tool_name == "create_leo_project":
                        if tool_result.output["success"]:
                            project_path = tool_result.output["project_path"]
                            project_paths[comp['name']] = project_path
                            
                            # If this is a composite project, set up dependencies
                            if dependencies:
                                # This would need to be implemented for actual composite projects
                                # For now, we'll just note the dependencies
                                console.print(f"[yellow]Note: Component {comp['name']} depends on {dep_string}[/yellow]")
        
        return project_paths
    
    def _sort_components_by_dependencies(self, components):
        """Sort components based on their dependencies."""
        # Simple topological sort
        result = []
        visited = set()
        
        def visit(component):
            if component['name'] in visited:
                return
            
            visited.add(component['name'])
            
            for dep_name in component.get('depends_on', []):
                # Find the dependency component
                dep_component = next((c for c in components if c['name'] == dep_name), None)
                if dep_component:
                    visit(dep_component)
            
            result.append(component)
        
        for component in components:
            visit(component)
        
        return result
    
    def _get_private_key(self):
        """Get private key from user with validation."""
        console.print("[bold]Please enter your Aleo private key (or leave empty to skip):[/bold]")
        console.print("[dim]Your private key will be used for deployment and is not stored.[/dim]")
        
        private_key = Prompt.ask("[bold]Private Key[/bold]", password=True, default="")
        
        if private_key and not verify_private_key(private_key):
            console.print("[bold red]Invalid private key format. Should start with 'APrivateKey'.[/bold red]")
            
            if Confirm.ask("[bold yellow]Would you like to try entering your private key again?[/bold yellow]"):
                return self._get_private_key()
            else:
                return None
        
        return private_key
    
    def _generate_code(self, project_paths, components):
        """Generate Leo code for each component using agents and handoffs."""
        console.print("[bold]Generating Leo code for components...[/bold]")
        
        generated_code = {}
        
        for comp in components["components"]:
            if comp['name'] not in project_paths:
                console.print(f"[bold red]Project path not found for component {comp['name']}. Skipping.[/bold red]")
                continue
                
            project_path = project_paths[comp['name']]
            
            # Prepare component-specific prompt
            dependencies = comp.get('depends_on', [])
            dependencies_info = ""
            
            if dependencies:
                dependencies_info = "This component depends on the following components: " + ", ".join(dependencies)
            
            component_prompt = f"""
            Component: {comp['name']}
            Purpose: {comp['purpose']}
            {dependencies_info}
            
            Please implement this component according to these requirements.
            """
            
            # Generate code for this component using the architect agent with handoff to generator
            result = Runner.run_sync(
                self.architect_agent,
                f"Analyze and generate Leo code for component: {comp['name']}\n\n{component_prompt}"
            )
            
            # Get the code from either direct output or from a handoff
            if result.handoff_results and result.handoff_results[0].final_output:
                # Code came from a handoff to the generator agent
                code = result.handoff_results[0].final_output
                
                # Clean up the code (remove markdown code blocks if present)
                if "```" in code:
                    # Extract only the code part
                    code_parts = code.split("```")
                    if len(code_parts) >= 3:
                        code = code_parts[1]
                        if code.startswith("leo"):
                            code = code[3:].strip()
            else:
                # Direct output from architect (less likely, but handle it)
                code = result.final_output
                if "```" in code:
                    # Extract only the code part
                    code_parts = code.split("```")
                    if len(code_parts) >= 3:
                        code = code_parts[1]
                        if code.startswith("leo"):
                            code = code[3:].strip()
            
            if code:
                # Add import statements for dependencies
                for dep in dependencies:
                    code = add_import_to_code(code, dep)
                
                generated_code[comp['name']] = code
                
                # Save the generated code to the project
                program_file_path = f"{project_path}/src/main.leo"
                save_leo_code(comp['name'], program_file_path, code)
        
        return generated_code
    
    def _evaluate_code(self, generated_code):
        """Evaluate the quality of generated code using the evaluator agent."""
        console.print("[bold]Evaluating generated Leo code...[/bold]")
        
        for comp_name, code in generated_code.items():
            console.print(f"[bold]Evaluating component: {comp_name}[/bold]")
            
            evaluation_prompt = f"""
            Evaluate the following Leo code for component {comp_name}:
            
            ```leo
            {code}
            ```
            
            Provide a detailed evaluation including:
            1. Correctness (Does it follow Leo syntax correctly?)
            2. Completeness (Does it implement all necessary features?)
            3. Security considerations
            4. Efficiency
            5. Readability and maintainability
            
            Also use the verify_leo_code tool to perform basic syntax validation.
            """
            
            result = Runner.run_sync(self.evaluator_agent, evaluation_prompt)
            
            # Display the evaluation
            console.print(Panel.fit(f"[bold yellow]Code Evaluation for {comp_name}:[/bold yellow]\n{result.final_output}", title="Evaluation"))
    
    def _build_projects(self, project_paths):
        """Build all Leo projects using the builder agent."""
        console.print("[bold]Building Leo projects...[/bold]")
        
        build_results = {}
        
        for comp_name, project_path in project_paths.items():
            console.print(f"[bold]Building component: {comp_name}[/bold]")
            
            build_prompt = f"""
            Build the Leo project for component: {comp_name}
            Project path: {project_path}
            
            Use the build_leo_project tool to build this project.
            """
            
            result = Runner.run_sync(self.builder_agent, build_prompt)
            
            # Check if the agent used the build_project_tool
            success = False
            for tool_result in result.tool_results:
                if tool_result.tool_name == "build_leo_project":
                    success = tool_result.output["success"]
                    if success:
                        console.print(f"[green]{tool_result.output['message']}[/green]")
                    else:
                        console.print(f"[red]{tool_result.output['message']}[/red]")
            
            build_results[comp_name] = success
        
        # Check if all builds were successful
        return all(build_results.values()) 