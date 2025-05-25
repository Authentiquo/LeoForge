"""
LeoForge CLI - Rich console interface for Leo project generation
"""
import asyncio
import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from src.models import UserQuery, ProjectType, ProjectResult
from src.workflow.orchestrator import ProjectOrchestrator


app = typer.Typer(
    name="leoforge",
    help="🚀 LeoForge - AI-powered Leo project generator",
    add_completion=False
)
console = Console()


def display_banner():
    """Display the LeoForge banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║                        🔥 LeoForge 🔥                        ║
    ║                                                               ║
    ║           AI-Powered Leo Smart Contract Generator             ║
    ║                    For Aleo Blockchain                        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def display_project_types():
    """Display available project types"""
    table = Table(title="Available Project Types", border_style="blue")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Example Use Cases", style="dim")
    
    project_info = {
        ProjectType.TOKEN: (
            "Fungible Token",
            "ERC20-like tokens, reward points, game currency"
        ),
        ProjectType.NFT: (
            "Non-Fungible Token",
            "Digital art, collectibles, membership passes"
        ),
        ProjectType.DEFI: (
            "DeFi Protocol",
            "AMM, lending, staking, yield farming"
        ),
        ProjectType.GAME: (
            "Gaming Contract",
            "On-chain games, loot boxes, tournaments"
        ),
        ProjectType.ORACLE: (
            "Oracle Service",
            "Price feeds, random numbers, external data"
        ),
        ProjectType.CUSTOM: (
            "Custom Project",
            "Any other type of smart contract"
        )
    }
    
    for ptype, (desc, examples) in project_info.items():
        table.add_row(ptype.value, desc, examples)
    
    console.print(table)


def display_result_summary(result: ProjectResult):
    """Display comprehensive project generation summary"""
    if result.success:
        console.print("\n[bold green]✨ Project Generation Complete! ✨[/bold green]\n")
        
        # Success summary
        summary_table = Table(title="Generation Summary", border_style="green")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("Project Name", result.project_name)
        summary_table.add_row("Status", "[green]Success[/green]")
        summary_table.add_row("Iterations", str(result.total_iterations))
        summary_table.add_row("Total Time", f"{result.total_duration:.2f}s")
        summary_table.add_row("Workspace", result.workspace_path or "N/A")
        
        console.print(summary_table)
        
        # Show final code snippet
        if result.final_code:
            code_lines = result.final_code.split('\n')
            snippet = '\n'.join(code_lines[:20])
            if len(code_lines) > 20:
                snippet += "\n// ... (truncated)"
            
            console.print("\n[bold]Code Preview:[/bold]")
            syntax = Syntax(snippet, "rust", theme="monokai", line_numbers=True)
            console.print(syntax)
        
        # Next steps
        console.print("\n[bold cyan]🎯 Next Steps:[/bold cyan]")
        console.print(f"1. Navigate to: [yellow]cd {result.project_name}[/yellow]")
        console.print("2. Review code: [yellow]cat src/main.leo[/yellow]")
        console.print("3. Test build: [yellow]leo build[/yellow]")
        console.print("4. Run tests: [yellow]leo test[/yellow]")
        
    else:
        console.print("\n[bold red]❌ Project Generation Failed[/bold red]\n")
        
        if result.error_message:
            console.print(Panel(
                result.error_message,
                title="[red]Error Details[/red]",
                border_style="red"
            ))
        
        # Show iteration history
        if result.iterations:
            console.print("\n[bold]Iteration History:[/bold]")
            for iteration in result.iterations:
                status = "✓" if iteration.success else "✗"
                console.print(
                    f"  {status} Iteration {iteration.iteration_number}: "
                    f"Score={iteration.evaluation.score:.1f}, "
                    f"Build={'Success' if iteration.success else 'Failed'}"
                )


@app.command("generate", help="🚀 Generate a new Leo project")
def generate(
    query: Optional[str] = typer.Argument(
        None,
        help="Natural language description of your project"
    ),
    project_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Project type (token, nft, defi, game, oracle, custom)"
    ),
    max_iterations: int = typer.Option(
        5, "--iterations", "-i",
        help="Maximum iterations for code generation"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive",
        help="Run in interactive mode"
    )
):
    """Generate a new Leo project using AI"""
    display_banner()
    
    # Get user input
    if interactive and not query:
        console.print("\n[bold cyan]Welcome to LeoForge Interactive Mode![/bold cyan]\n")
        
        # Show project types
        display_project_types()
        
        # Get project description
        query = Prompt.ask(
            "\n[bold]Describe your project[/bold]",
            default="Create a simple token with mint and transfer functions"
        )
        
        # Get project type
        if not project_type:
            project_type = Prompt.ask(
                "[bold]Select project type[/bold]",
                choices=[t.value for t in ProjectType],
                default=ProjectType.CUSTOM.value
            )
    
    if not query:
        console.print("[red]Error: Project description is required[/red]")
        raise typer.Exit(1)
    
    # Parse project type
    try:
        ptype = ProjectType(project_type) if project_type else None
    except ValueError:
        ptype = None
    
    # Create user query
    user_query = UserQuery(
        query=query,
        project_type=ptype
    )
    
    # Run generation
    console.print("\n[bold green]Starting project generation...[/bold green]\n")
    
    orchestrator = ProjectOrchestrator(max_iterations=max_iterations, console=console)
    result = asyncio.run(orchestrator.generate_project(user_query))
    
    # Display results
    display_result_summary(result)
    
    # Exit with appropriate code
    raise typer.Exit(0 if result.success else 1)


@app.command("examples", help="📚 Show example project queries")
def examples():
    """Show example project generation queries"""
    display_banner()
    
    examples_data = [
        ("Token", "Create an ERC20-like token with mint, burn, and transfer functions"),
        ("NFT", "Build an NFT collection with minting, transfers, and metadata"),
        ("DeFi", "Implement a simple AMM DEX with liquidity pools and swaps"),
        ("Game", "Create a dice game with betting and random number generation"),
        ("Oracle", "Build a price oracle that stores ETH/USD price data"),
        ("Voting", "Implement a DAO voting system with proposals and weighted votes"),
        ("Escrow", "Create an escrow service for secure peer-to-peer transactions"),
        ("Lottery", "Build a decentralized lottery with ticket purchases and payouts")
    ]
    
    table = Table(title="Example Project Queries", border_style="blue")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Query", style="white")
    
    for category, query in examples_data:
        table.add_row(category, query)
    
    console.print(table)
    
    console.print("\n[bold]Usage:[/bold]")
    console.print('  leoforge generate "Your project description here"')
    console.print('  leoforge generate --type token "Create a governance token"')


@app.command("version", help="📌 Show LeoForge version")
def version():
    """Display version information"""
    from src import __version__
    
    console.print(f"[bold cyan]LeoForge[/bold cyan] version [green]{__version__}[/green]")
    console.print("[dim]AI-Powered Leo Smart Contract Generator[/dim]")


def main():
    """Main entry point"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main() 