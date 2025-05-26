"""
Project Orchestrator - Manages the complete code generation workflow
"""
import asyncio
import time
from typing import Optional, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from src.models import (
    UserQuery, CodeRequirements, ProjectResult, 
    IterationResult
)
from src.leoagents.architect import ArchitectAgent
from src.leoagents.code_generator import CodeGeneratorAgent
from src.leoagents.code_evaluator import CodeEvaluatorAgent
from src.services.builder import WorkspaceManager, LeoBuilder


class ProjectOrchestrator:
    """Orchestrates the complete Leo project generation workflow"""
    
    def __init__(self, max_iterations: int = 5, console: Optional[Console] = None):
        self.max_iterations = max_iterations
        self.console = console or Console()
        
        # Initialize agents
        self.architect = ArchitectAgent()
        self.generator = CodeGeneratorAgent()
        self.evaluator = CodeEvaluatorAgent()
        
        # Initialize services
        self.workspace_manager = WorkspaceManager()
        self.builder = LeoBuilder()
    
    async def generate_project(self, user_query: UserQuery) -> ProjectResult:
        """Execute the complete project generation workflow"""
        start_time = time.time()
        
        self.console.print(Panel.fit(
            f"[bold cyan]🚀 LeoForge Project Generation[/bold cyan]\n"
            f"[dim]Query: {user_query.query}[/dim]",
            border_style="cyan"
        ))
        
        try:
            # Step 1: Architecture Design
            with self.console.status("[bold green]🏗️  Designing architecture..."):
                architecture = await self.architect.design_architecture(user_query)
                self.console.print("[green]✓[/green] Architecture design complete")
            
            # Create normalized requirements
            requirements = CodeRequirements(
                project_name=architecture.project_name,
                description=architecture.description,
                features=architecture.features,
                architecture=architecture
            )
            
            # Display architecture
            self._display_architecture(architecture)
            
            # Step 2: Create Workspace
            success, workspace_path = self.workspace_manager.create_workspace(requirements.project_name)
            if not success:
                return ProjectResult(
                    success=False,
                    project_name=requirements.project_name,
                    error_message=workspace_path
                )
            
            self.console.print(f"[green]✓[/green] Workspace created: [dim]{workspace_path}[/dim]")
            
            # Step 3: Generation Loop
            iterations = []
            final_code = None
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                
                for iteration_num in range(1, self.max_iterations + 1):
                    task = progress.add_task(
                        f"[cyan]Iteration {iteration_num}/{self.max_iterations}",
                        total=None
                    )
                    
                    iteration_start = time.time()
                    
                    # Generate or fix code
                    if iteration_num == 1:
                        progress.update(task, description="[yellow]Generating initial code...")
                        generated = await self.generator.generate_code(requirements)
                    else:
                        progress.update(task, description="[yellow]Fixing compilation errors...")
                        generated = await self.generator.fix_compilation_errors(
                            final_code,
                            iterations[-1].build,
                            requirements
                        )
                    
                    # Save code
                    self.workspace_manager.save_code(requirements.project_name, generated.code)
                    final_code = generated.code
                    
                    # Evaluate code
                    progress.update(task, description="[yellow]Evaluating code quality...")
                    evaluation = await self.evaluator.evaluate_code(generated, requirements)
                    
                    # Build project if evaluation passes minimum threshold
                    build_result = None
                    if evaluation.score >= 50:
                        progress.update(task, description="[yellow]Building project...")
                        build_result = self.builder.build_project(requirements.project_name)
                    
                    # Create iteration result
                    iteration_result = IterationResult(
                        iteration_number=iteration_num,
                        code=generated,
                        evaluation=evaluation,
                        build=build_result,
                        success=build_result and build_result.success,
                        duration=time.time() - iteration_start
                    )
                    
                    iterations.append(iteration_result)
                    progress.remove_task(task)
                    
                    # Display iteration results
                    self._display_iteration_result(iteration_result)
                    
                    # Check for success
                    if iteration_result.success:
                        self.console.print(
                            f"\n[bold green]🎉 Success![/bold green] "
                            f"Project built successfully in {iteration_num} iteration(s)"
                        )
                        break
                    
                    # Continue iterating if we have build errors and haven't reached max iterations
                    # Only stop early if evaluation score is very low (< 50) indicating fundamental issues
                    if iteration_num == self.max_iterations:
                        if build_result and not build_result.success:
                            self.console.print(
                                f"\n[yellow]⚠️  Reached maximum iterations ({self.max_iterations}). "
                                f"Build still failing. Manual intervention may be required.[/yellow]"
                            )
                        elif evaluation.score >= 70:
                            self.console.print(
                                f"\n[yellow]⚠️  Code evaluation passed but build failed. "
                                f"Manual intervention may be required.[/yellow]"
                            )
                    elif evaluation.score < 50:
                        self.console.print(
                            f"\n[red]⚠️  Code quality too low (score: {evaluation.score:.1f}). "
                            f"Stopping iterations.[/red]"
                        )
                        break
            
            # Create final result
            total_duration = time.time() - start_time
            success = any(i.success for i in iterations)
            
            return ProjectResult(
                success=success,
                project_name=requirements.project_name,
                final_code=final_code,
                iterations=iterations,
                total_iterations=len(iterations),
                total_duration=total_duration,
                workspace_path=workspace_path if success else None
            )
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
            return ProjectResult(
                success=False,
                project_name=user_query.query[:20] + "...",
                error_message=str(e),
                total_duration=time.time() - start_time
            )
    
    def _display_architecture(self, architecture):
        """Display architecture design in a formatted table"""
        table = Table(title="Project Architecture", border_style="blue")
        table.add_column("Component", style="cyan")
        table.add_column("Details", style="white")
        
        table.add_row("Project Name", architecture.project_name)
        table.add_row("Type", architecture.project_type.value)
        table.add_row("Features", "\n".join(f"• {f}" for f in architecture.features))
        
        if architecture.data_structures:
            table.add_row(
                "Data Structures",
                "\n".join(f"• {k}: {v}" for k, v in architecture.data_structures.items())
            )
        
        if architecture.transitions:
            table.add_row(
                "Transitions",
                "\n".join(f"• {k}: {v}" for k, v in architecture.transitions.items())
            )
        
        self.console.print(table)
    
    def _display_iteration_result(self, result: IterationResult):
        """Display results of a single iteration"""
        # Create summary table
        table = Table(title=f"Iteration {result.iteration_number} Results", border_style="blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        # Evaluation metrics
        table.add_row("Code Quality Score", f"{result.evaluation.score:.1f}/100")
        table.add_row("Complete", "✓" if result.evaluation.is_complete else "✗")
        table.add_row("Has Errors", "✗" if result.evaluation.has_errors else "✓")
        
        # Build status
        if result.build:
            status_color = "green" if result.build.success else "red"
            table.add_row(
                "Build Status",
                f"[{status_color}]{result.build.status.value}[/{status_color}]"
            )
            table.add_row("Build Time", f"{result.build.build_time:.2f}s")
        else:
            table.add_row("Build Status", "[dim]Not attempted[/dim]")
        
        table.add_row("Duration", f"{result.duration:.2f}s")
        
        self.console.print(table)
        
        # Show issues if any
        if result.evaluation.missing_features:
            self.console.print(
                Panel(
                    "\n".join(f"• {f}" for f in result.evaluation.missing_features),
                    title="[yellow]Missing Features[/yellow]",
                    border_style="yellow"
                )
            )
        
        if result.evaluation.improvements:
            self.console.print(
                Panel(
                    "\n".join(f"• {i}" for i in result.evaluation.improvements[:3]),
                    title="[cyan]Suggested Improvements[/cyan]",
                    border_style="cyan"
                )
            )
        
        if result.build and not result.build.success and result.build.errors:
            self.console.print(
                Panel(
                    "\n".join(result.build.errors[:3]),
                    title="[red]Build Errors[/red]",
                    border_style="red"
                )
            ) 