"""
Example usage of the enhanced LeoForge with error logging and rule learning
"""
import asyncio
from src.workflow import ProjectOrchestrator
from src.models import UserQuery, ProjectType
from src.services import LeoLogger, RuleManager
from rich.console import Console

console = Console()

async def main():
    """Example of using LeoForge with logging and rule learning"""
    
    # Create orchestrator
    orchestrator = ProjectOrchestrator(max_iterations=5, console=console)
    
    # Example query
    user_query = UserQuery(
        query="Create a Leo NFT contract with minting and transfer functions",
        project_type=ProjectType.NFT
    )
    
    # Generate project - the logging and rule learning happens automatically
    result = await orchestrator.generate_project(user_query)
    
    # The system will:
    # 1. Log all errors encountered during generation
    # 2. Track code versions at each iteration
    # 3. Record the resolution path
    # 4. After completion (success or failure), analyze the logs
    # 5. Generate rules for Architect and Code Generator agents
    # 6. Save rules persistently for future runs
    
    if result.success:
        console.print(f"[green]✅ Project generated successfully![/green]")
        console.print(f"Workspace: {result.workspace_path}")
        console.print(f"Total iterations: {result.total_iterations}")
    else:
        console.print(f"[red]❌ Project generation failed[/red]")
        console.print(f"Error: {result.error_message}")
    
    # Show available rules after the run
    rule_manager = RuleManager()
    architect_rules = rule_manager.get_architect_rules(limit=3)
    codex_rules = rule_manager.get_codex_rules(limit=3)
    
    if architect_rules:
        console.print("\n[cyan]Top Architect Rules Learned:[/cyan]")
        for rule in architect_rules:
            console.print(f"  • {rule.title}: {rule.description}")
    
    if codex_rules:
        console.print("\n[cyan]Top Code Generator Rules Learned:[/cyan]")
        for rule in codex_rules:
            console.print(f"  • {rule.title}: {rule.description}")
    
    # View recent logs
    logger = LeoLogger()
    recent_runs = logger.get_recent_runs(limit=3)
    
    console.print(f"\n[dim]Recent runs logged: {len(recent_runs)}[/dim]")
    for run in recent_runs:
        console.print(f"  • {run.project_name}: {'✅' if run.success else '❌'} ({len(run.error_logs)} errors)")

if __name__ == "__main__":
    asyncio.run(main()) 