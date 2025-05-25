#!/usr/bin/env python3
"""
LeoForge Demo - Simple demonstration of the system
"""
import asyncio
from rich.console import Console
from src.models import UserQuery, ProjectType
from src.workflow.orchestrator import ProjectOrchestrator


async def demo():
    """Run a simple demo of LeoForge"""
    console = Console()
    
    # Display banner
    console.print("\n[bold cyan]🔥 LeoForge Demo 🔥[/bold cyan]\n")
    
    # Create a simple user query
    user_query = UserQuery(
        query="Create a simple token with mint and transfer functions, include a total supply limit",
        project_type=ProjectType.TOKEN
    )
    
    console.print(f"[bold]Demo Query:[/bold] {user_query.query}")
    console.print(f"[bold]Project Type:[/bold] {user_query.project_type.value}\n")
    
    # Create orchestrator with max 2 iterations for demo
    orchestrator = ProjectOrchestrator(max_iterations=2, console=console)
    
    # Generate project
    console.print("[yellow]Starting project generation...[/yellow]\n")
    result = await orchestrator.generate_project(user_query)
    
    # Display summary
    if result.success:
        console.print(f"\n[bold green]✅ Demo completed successfully![/bold green]")
        console.print(f"Project: {result.project_name}")
        console.print(f"Iterations: {result.total_iterations}")
        console.print(f"Time: {result.total_duration:.2f}s")
    else:
        console.print(f"\n[bold red]❌ Demo failed[/bold red]")
        if result.error_message:
            console.print(f"Error: {result.error_message}")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo()) 