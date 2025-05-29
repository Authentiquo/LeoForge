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
import json
from datetime import datetime

from src.models import UserQuery, ProjectType, ProjectResult
from src.workflow.orchestrator import ProjectOrchestrator
from src.config import get_config, update_admin_address
from src.services.logger import LeoLogger
from src.services.rule_manager import RuleManager
from src.leoagents.rule_engineer import RuleEngineerAgent


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
        console.print(f"1. Navigate to: [yellow]cd output/{result.project_name}[/yellow]")
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


@app.command("config", help="⚙️ Show or update configuration")
def config(
    show_admin: bool = typer.Option(
        False, "--admin", "-a",
        help="Show admin configuration"
    ),
    set_admin: Optional[str] = typer.Option(
        None, "--set-admin",
        help="Set new admin address"
    )
):
    """Show or update LeoForge configuration"""
    display_banner()
    
    config_obj = get_config()
    
    if set_admin:
        if update_admin_address(set_admin):
            console.print(f"[green]✓ Admin address updated to: {set_admin}[/green]")
        else:
            console.print(f"[red]✗ Invalid Aleo address format: {set_admin}[/red]")
            console.print("[dim]Address should start with 'aleo1' and be 63 characters long[/dim]")
            raise typer.Exit(1)
        return
    
    # Show configuration
    config_table = Table(title="LeoForge Configuration", border_style="blue")
    config_table.add_column("Setting", style="cyan", no_wrap=True)
    config_table.add_column("Value", style="white")
    config_table.add_column("Description", style="dim")
    
    # API Keys (masked for security)
    anthropic_key = "***configured***" if config_obj.anthropic_api_key else "[red]not set[/red]"
    openai_key = "***configured***" if config_obj.openai_api_key else "[red]not set[/red]"
    
    config_table.add_row("Anthropic API Key", anthropic_key, "For Claude models")
    config_table.add_row("OpenAI API Key", openai_key, "For GPT models")
    
    if show_admin or True:  # Always show admin info for now
        config_table.add_row("Admin Address", config_obj.admin_address, "Default admin address for contracts")
        config_table.add_row("Max Iterations", str(config_obj.max_iterations), "Maximum generation iterations")
        config_table.add_row("Build Timeout", f"{config_obj.build_timeout}s", "Timeout for build operations")
    
    console.print(config_table)
    
    # Validation status
    api_status = "✓ Valid" if config_obj.validate_api_keys() else "✗ No API keys configured"
    admin_status = "✓ Valid" if config_obj.is_valid_aleo_address(config_obj.admin_address) else "✗ Invalid format"
    
    status_table = Table(title="Validation Status", border_style="green")
    status_table.add_column("Component", style="cyan")
    status_table.add_column("Status", style="white")
    
    status_table.add_row("API Keys", api_status)
    status_table.add_row("Admin Address", admin_status)
    
    console.print(status_table)
    
    # Usage examples
    console.print("\n[bold]Usage Examples:[/bold]")
    console.print("  leoforge config --admin                     # Show admin configuration")
    console.print("  leoforge config --set-admin <address>       # Update admin address")


@app.command("analyze-logs", help="🧠 Analyze logs and generate rules from errors")
def analyze_logs(
    log_file: Optional[str] = typer.Argument(
        None,
        help="Specific log file to analyze (e.g., 'project_name_uuid.json')"
    ),
    list_logs: bool = typer.Option(
        False, "--list", "-l",
        help="List available log files"
    ),
    filter_errors_only: bool = typer.Option(
        True, "--errors-only/--all",
        help="Only analyze logs with build errors that resulted in successful builds"
    )
):
    """Analyze error logs and generate improvement rules"""
    display_banner()
    
    logger = LeoLogger()
    
    if list_logs:
        # List available log files
        recent_runs = logger.get_recent_runs(limit=20)
        
        if not recent_runs:
            console.print("[yellow]No log files found[/yellow]")
            return
        
        table = Table(title="Available Log Files", border_style="blue")
        table.add_column("Project Name", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Errors", style="yellow")
        table.add_column("Date", style="dim")
        table.add_column("File", style="dim")
        
        for run in recent_runs:
            status = "✅ Success" if run.success else "❌ Failed"
            build_error_count = len([e for e in run.error_logs if e.error_type == "build"])
            date = run.start_time.strftime("%Y-%m-%d %H:%M")
            filename = f"{run.project_name}_{run.run_id}.json"
            
            # Apply filter if requested - only show logs with build errors that resulted in success
            if filter_errors_only and (build_error_count == 0 or not run.success):
                continue
                
            table.add_row(
                run.project_name,
                status,
                str(build_error_count),
                date,
                filename
            )
        
        console.print(table)
        
        console.print("\n[bold]Usage:[/bold]")
        console.print("  leoforge analyze-logs <filename>")
        console.print("  leoforge analyze-logs --errors-only")
        return
    
    if not log_file:
        # Auto-select logs with errors that resulted in successful builds
        recent_runs = logger.get_recent_runs(limit=10)
        eligible_runs = [
            run for run in recent_runs 
            if len([e for e in run.error_logs if e.error_type == "build"]) > 0 and run.success
        ]
        
        if not eligible_runs:
            console.print("[yellow]No eligible log files found (need logs with build errors that resulted in successful builds)[/yellow]")
            console.print("\nUse [cyan]leoforge analyze-logs --list[/cyan] to see all available logs")
            return
        
        # Show eligible runs and let user choose
        console.print("[bold cyan]Eligible logs for analysis:[/bold cyan]\n")
        
        table = Table(border_style="green")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Project", style="white")
        table.add_column("Errors", style="yellow", width=8)
        table.add_column("Date", style="dim")
        
        for i, run in enumerate(eligible_runs, 1):
            date = run.start_time.strftime("%Y-%m-%d %H:%M")
            build_error_count = len([e for e in run.error_logs if e.error_type == "build"])
            table.add_row(str(i), run.project_name, str(build_error_count), date)
        
        console.print(table)
        
        choice = Prompt.ask(
            "\n[bold]Select log to analyze[/bold]",
            choices=[str(i) for i in range(1, len(eligible_runs) + 1)],
            default="1"
        )
        
        selected_run = eligible_runs[int(choice) - 1]
        log_file = f"{selected_run.project_name}_{selected_run.run_id}.json"
    
    # Load and analyze the specific log file
    try:
        run_log = logger.load_run_log(log_file)
        
        if not run_log:
            console.print(f"[red]Error: Log file '{log_file}' not found[/red]")
            return
        
        # Check if log meets criteria
        build_errors = [e for e in run_log.error_logs if e.error_type == "build"]
        if filter_errors_only and (len(build_errors) == 0 or not run_log.success):
            console.print(f"[yellow]Log '{log_file}' doesn't meet criteria (no build errors or failed build)[/yellow]")
            return
        
        # Display log summary
        console.print(f"\n[bold green]Analyzing log: {log_file}[/bold green]\n")
        
        summary_table = Table(title="Log Summary", border_style="blue")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("Project", run_log.project_name)
        summary_table.add_row("Status", "✅ Success" if run_log.success else "❌ Failed")
        summary_table.add_row("Build Errors", str(len(build_errors)))
        summary_table.add_row("Total Errors", str(len(run_log.error_logs)))
        summary_table.add_row("Code Versions", str(len(run_log.code_versions)))
        summary_table.add_row("Resolution Steps", str(len(run_log.resolution_path)))
        
        console.print(summary_table)
        
        # Show build errors only
        if build_errors:
            console.print("\n[bold yellow]Build errors encountered:[/bold yellow]")
            for i, error in enumerate(build_errors, 1):
                console.print(f"  {i}. [red]{error.error_type}[/red]: {error.error_message}")
        
        if len(run_log.error_logs) > len(build_errors):
            console.print(f"\n[dim]Note: {len(run_log.error_logs) - len(build_errors)} evaluation errors were also logged but are not shown[/dim]")
        
        # Confirm analysis
        if not Confirm.ask("\n[bold]Proceed with rule generation?[/bold]", default=True):
            return
        
        # Analyze and generate rules
        console.print("\n[bold blue]🧠 Analyzing errors and generating rules...[/bold blue]")
        
        rule_engineer = RuleEngineerAgent()
        analysis = asyncio.run(rule_engineer.analyze_run_log(run_log))
        
        # Display results
        if analysis.architect_rules:
            console.print(f"\n[bold cyan]✨ Generated {len(analysis.architect_rules)} Architect Rules:[/bold cyan]")
            for i, rule in enumerate(analysis.architect_rules, 1):
                console.print(f"\n{i}. [bold]{rule.title}[/bold]")
                console.print(f"   📝 {rule.description}")
                console.print(f"   🎯 Solution: {rule.solution}")
                console.print(f"   ⭐ Priority: {rule.priority}/10")
        
        if analysis.codex_rules:
            console.print(f"\n[bold cyan]✨ Generated {len(analysis.codex_rules)} Code Generator Rules:[/bold cyan]")
            for i, rule in enumerate(analysis.codex_rules, 1):
                console.print(f"\n{i}. [bold]{rule.title}[/bold]")
                console.print(f"   📝 {rule.description}")
                console.print(f"   🎯 Solution: {rule.solution}")
                console.print(f"   ⭐ Priority: {rule.priority}/10")
        
        if analysis.general_observations:
            console.print(f"\n[bold yellow]📊 General Observations:[/bold yellow]")
            for obs in analysis.general_observations:
                console.print(f"  • {obs}")
        
        # Show total rules count
        rule_manager = RuleManager()
        total_architect = len(rule_manager.get_architect_rules())
        total_codex = len(rule_manager.get_codex_rules())
        
        console.print(f"\n[bold green]✅ Rules saved successfully![/bold green]")
        console.print(f"Total rules: {total_architect} architect, {total_codex} code generator")
        
    except Exception as e:
        console.print(f"[bold red]Error analyzing log:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("rules", help="📋 Manage and view generated rules")
def rules(
    list_rules: bool = typer.Option(
        True, "--list/--no-list", "-l",
        help="List all generated rules"
    ),
    rule_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Filter by rule type (architect, codex)"
    ),
    clear_rules: bool = typer.Option(
        False, "--clear",
        help="Clear all rules (requires confirmation)"
    ),
    export_rules: Optional[str] = typer.Option(
        None, "--export",
        help="Export rules to a file"
    )
):
    """Manage and view generated improvement rules"""
    display_banner()
    
    rule_manager = RuleManager()
    
    if clear_rules:
        if Confirm.ask("[bold red]Are you sure you want to clear all rules?[/bold red]", default=False):
            # Clear rules by overwriting with empty lists
            rule_manager.save_rules([], [])
            console.print("[green]✅ All rules cleared[/green]")
        return
    
    if export_rules:
        try:
            architect_rules = rule_manager.get_architect_rules()
            codex_rules = rule_manager.get_codex_rules()
            
            export_data = {
                "architect_rules": [rule.dict() for rule in architect_rules],
                "codex_rules": [rule.dict() for rule in codex_rules],
                "exported_at": datetime.now().isoformat(),
                "total_rules": len(architect_rules) + len(codex_rules)
            }
            
            with open(export_rules, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            console.print(f"[green]✅ Rules exported to {export_rules}[/green]")
            console.print(f"Total rules exported: {len(architect_rules)} architect, {len(codex_rules)} codex")
            return
            
        except Exception as e:
            console.print(f"[red]Error exporting rules: {e}[/red]")
            return
    
    if list_rules:
        architect_rules = rule_manager.get_architect_rules()
        codex_rules = rule_manager.get_codex_rules()
        
        # Filter by type if specified
        if rule_type == "architect":
            codex_rules = []
        elif rule_type == "codex":
            architect_rules = []
        elif rule_type and rule_type not in ["architect", "codex"]:
            console.print(f"[red]Invalid rule type: {rule_type}. Use 'architect' or 'codex'[/red]")
            return
        
        if not architect_rules and not codex_rules:
            console.print("[yellow]No rules found[/yellow]")
            console.print("\nGenerate rules with: [cyan]leoforge analyze-logs[/cyan]")
            return
        
        # Display architect rules
        if architect_rules:
            console.print(f"\n[bold cyan]🏗️  Architect Rules ({len(architect_rules)})[/bold cyan]")
            
            table = Table(border_style="cyan")
            table.add_column("#", style="dim", width=3)
            table.add_column("Title", style="white")
            table.add_column("Priority", style="yellow", width=8)
            table.add_column("Tags", style="dim")
            
            for i, rule in enumerate(architect_rules, 1):
                tags = ", ".join(rule.tags[:3])  # Show first 3 tags
                if len(rule.tags) > 3:
                    tags += "..."
                table.add_row(str(i), rule.title, f"{rule.priority}/10", tags)
            
            console.print(table)
            
            # Show detailed view of top 3 rules
            console.print("\n[bold]Top 3 Architect Rules (detailed):[/bold]")
            for i, rule in enumerate(architect_rules[:3], 1):
                console.print(f"\n{i}. [bold]{rule.title}[/bold]")
                console.print(f"   📝 {rule.description}")
                console.print(f"   🚫 Pattern to avoid: {rule.pattern}")
                console.print(f"   ✅ Solution: {rule.solution}")
                if rule.examples:
                    console.print(f"   💡 Example: {rule.examples[0]}")
        
        # Display codex rules
        if codex_rules:
            console.print(f"\n[bold cyan]⚙️  Code Generator Rules ({len(codex_rules)})[/bold cyan]")
            
            table = Table(border_style="cyan")
            table.add_column("#", style="dim", width=3)
            table.add_column("Title", style="white")
            table.add_column("Priority", style="yellow", width=8)
            table.add_column("Tags", style="dim")
            
            for i, rule in enumerate(codex_rules, 1):
                tags = ", ".join(rule.tags[:3])  # Show first 3 tags
                if len(rule.tags) > 3:
                    tags += "..."
                table.add_row(str(i), rule.title, f"{rule.priority}/10", tags)
            
            console.print(table)
            
            # Show detailed view of top 3 rules
            console.print("\n[bold]Top 3 Code Generator Rules (detailed):[/bold]")
            for i, rule in enumerate(codex_rules[:3], 1):
                console.print(f"\n{i}. [bold]{rule.title}[/bold]")
                console.print(f"   📝 {rule.description}")
                console.print(f"   🚫 Pattern to avoid: {rule.pattern}")
                console.print(f"   ✅ Solution: {rule.solution}")
                if rule.examples:
                    console.print(f"   💡 Example: {rule.examples[0]}")
        
        # Summary
        total_rules = len(architect_rules) + len(codex_rules)
        console.print(f"\n[bold green]📊 Total Rules: {total_rules}[/bold green]")
        console.print(f"   🏗️  Architect: {len(architect_rules)}")
        console.print(f"   ⚙️  Code Generator: {len(codex_rules)}")
        
        console.print("\n[bold]Usage:[/bold]")
        console.print("  leoforge rules --type architect     # Show only architect rules")
        console.print("  leoforge rules --export rules.json  # Export rules to file")
        console.print("  leoforge rules --clear              # Clear all rules")


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