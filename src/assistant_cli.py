#!/usr/bin/env python3
"""
CLI for testing the Leo Assistant Agent
"""

import os
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from agents.assistant_agent import LeoAssistantAgent

# Load environment variables
load_dotenv()

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Leo code generator using OpenAI Assistant")
    parser.add_argument("--project", "-p", help="Project name", required=False)
    parser.add_argument("--requirements", "-r", help="File containing project requirements", required=False)
    args = parser.parse_args()
    
    console.print(Panel.fit(
        "[bold blue]Leo Assistant Agent[/bold blue]",
        subtitle="Generate Leo code using OpenAI Assistants API"
    ))
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.[/bold red]")
        return
    
    # Get project name if not provided
    project_name = args.project
    if not project_name:
        project_name = Prompt.ask("[bold]Enter a name for your Leo project[/bold]")
    
    # Get requirements if not provided
    requirements = ""
    if args.requirements:
        try:
            with open(args.requirements, 'r') as file:
                requirements = file.read()
        except FileNotFoundError:
            console.print(f"[bold red]Requirements file not found: {args.requirements}[/bold red]")
            return
    else:
        console.print("[bold yellow]Please describe your smart contract requirements:[/bold yellow]")
        console.print("[dim]Be specific about the functionality, records, and functions you need.[/dim]")
        requirements = console.input("")
    
    # Create agent and generate code
    agent = LeoAssistantAgent()
    thread_id = agent.generate_code(project_name, requirements)
    
    console.print(f"[bold green]Thread ID: {thread_id}[/bold green]")
    console.print("[bold green]Leo code generation completed![/bold green]")

if __name__ == "__main__":
    main() 