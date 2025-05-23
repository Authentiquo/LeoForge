import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from agents import AgentsConfig

from agents.workflow import LeoWorkflow

# Load environment variables
load_dotenv()

console = Console()

def main():
    console.print(Panel.fit(
        "[bold blue]Welcome to LeoForge[/bold blue]",
        subtitle="AI-powered Leo code generator for Aleo blockchain"
    ))
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.[/bold red]")
        return
    
    # Initialize the Agents SDK
    AgentsConfig.api_key = api_key
    
    # Optional: Enable tracing for debugging
    if os.getenv("ENABLE_TRACING", "false").lower() == "true":
        console.print("[dim]Enabling OpenAI Agents tracing for debugging[/dim]")
        AgentsConfig.enable_tracing = True
    
    # Get user input for project requirements
    project_name = Prompt.ask("[bold]Enter a name for your Leo project[/bold]")
    console.print("[bold yellow]Please describe your smart contract requirements:[/bold yellow]")
    console.print("[dim]Be specific about the functionality, records, and functions you need.[/dim]")
    user_input = console.input("")
    
    # Initialize workflow
    workflow = LeoWorkflow()
    workflow.execute_workflow(project_name, user_input)

if __name__ == "__main__":
    main() 