import os
import time
from openai import OpenAI
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

from ..tools.agent_tools import leo_tools, tool_functions

console = Console()

class LeoAssistantAgent:
    """Leo code generator agent using OpenAI's Assistants API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant = self._create_assistant()
        
    def _create_assistant(self):
        """Create or get an OpenAI Assistant for Leo code generation."""
        console.print("[bold]Setting up OpenAI Assistant for Leo code generation...[/bold]")
        
        # Load system prompt
        prompt_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "system_prompt.md")
        try:
            with open(prompt_file, 'r') as file:
                system_prompt = file.read()
        except FileNotFoundError:
            console.print(f"[bold red]System prompt file not found: {prompt_file}[/bold red]")
            system_prompt = "You are an expert in the Leo programming language for Aleo blockchain."
        
        # Check if the assistant already exists
        assistants = self.client.beta.assistants.list(
            order="desc",
            limit=10
        )
        
        for assistant in assistants.data:
            if assistant.name == "Leo Code Generator":
                console.print("[green]Found existing Leo Code Generator assistant[/green]")
                return assistant
        
        # Create a new assistant
        console.print("[yellow]Creating new Leo Code Generator assistant...[/yellow]")
        assistant = self.client.beta.assistants.create(
            name="Leo Code Generator",
            instructions=system_prompt,
            tools=leo_tools,
            model="gpt-4-turbo"
        )
        
        console.print("[green]Successfully created Leo Code Generator assistant[/green]")
        return assistant
    
    def generate_code(self, project_name, user_requirements):
        """Generate Leo code using the OpenAI Assistant."""
        console.print(Panel.fit(
            f"[bold blue]Generating Leo code for {project_name}[/bold blue]",
            subtitle="Using OpenAI Assistants API"
        ))
        
        # Create a new thread
        thread = self.client.beta.threads.create()
        
        # Add a message to the thread
        message_content = f"""
        Generate Leo code for a project named: {project_name}
        
        Requirements:
        {user_requirements}
        
        Please create a well-structured Leo program that implements these requirements.
        After generating the code, please evaluate its quality.
        """
        
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_content
        )
        
        # Run the assistant
        with Progress() as progress:
            task = progress.add_task("[green]Generating Leo code...", total=100)
            
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )
            
            # Poll for the run to complete
            while run.status in ["queued", "in_progress"]:
                progress.update(task, advance=5)
                time.sleep(1)
                
                # Check for required actions (tool calls)
                if run.status == "requires_action":
                    tool_outputs = []
                    
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        arguments = tool_call.function.arguments
                        
                        # Parse the arguments as a dictionary
                        import json
                        args_dict = json.loads(arguments)
                        
                        # Call the appropriate function
                        if function_name in tool_functions:
                            result = tool_functions[function_name](**args_dict)
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(result)
                            })
                    
                    # Submit the tool outputs
                    run = self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                else:
                    # Update the run status
                    run = self.client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )
            
            progress.update(task, completed=100)
        
        # Retrieve the messages
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Extract the assistant's response
        for message in messages.data:
            if message.role == "assistant":
                for content in message.content:
                    if content.type == "text":
                        console.print(Panel.fit(
                            content.text.value,
                            title="Assistant Response",
                            subtitle="Leo Code Generation"
                        ))
        
        return thread.id 