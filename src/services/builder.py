"""
Builder Service - Handles Leo compilation and workspace management
"""
import subprocess
import time
from pathlib import Path
from typing import Optional, List
from src.models import BuildResult, CompilationStatus, GeneratedCode


class WorkspaceManager:
    """Manages Leo project workspaces"""
    
    # Dossier de base pour tous les workspaces
    OUTPUT_DIR = "output"
    
    @staticmethod
    def _get_workspace_path(project_name: str) -> Path:
        """Get the full workspace path for a project"""
        output_dir = Path(WorkspaceManager.OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)  # Créer le dossier output s'il n'existe pas
        return output_dir / project_name
    
    @staticmethod
    def create_workspace(project_name: str) -> tuple[bool, str]:
        """Create a new Leo workspace in the output directory"""
        workspace_path = WorkspaceManager._get_workspace_path(project_name)
        
        if workspace_path.exists():
            return True, str(workspace_path.resolve())
        
        try:
            # Créer le dossier output s'il n'existe pas
            workspace_path.parent.mkdir(exist_ok=True)
            
            result = subprocess.run(
                ["leo", "new", project_name],
                cwd=workspace_path.parent,  # Exécuter dans le dossier output
                capture_output=True,
                text=True,
                check=True
            )
            return True, str(workspace_path.resolve())
        except subprocess.CalledProcessError as e:
            return False, f"Failed to create workspace: {e.stderr}"
        except FileNotFoundError:
            return False, "Leo CLI not found. Please install Leo first."
    
    @staticmethod
    def save_code(project_name: str, code: str) -> bool:
        """Save code to workspace main.leo file"""
        try:
            # Format the code before saving
            formatted_code = code.replace('\\n', '\n')
            
            # Clean up any double newlines that might have been created
            while '\n\n\n' in formatted_code:
                formatted_code = formatted_code.replace('\n\n\n', '\n\n')
            
            # Ensure proper spacing around braces
            formatted_code = formatted_code.replace('}{', '}\n{')
            formatted_code = formatted_code.strip()
            
            workspace_path = WorkspaceManager._get_workspace_path(project_name)
            file_path = workspace_path / "src" / "main.leo"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(formatted_code, encoding="utf-8")
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def read_code(project_name: str, file_path: str = "src/main.leo") -> Optional[str]:
        """Read code from workspace"""
        try:
            workspace_path = WorkspaceManager._get_workspace_path(project_name)
            full_path = workspace_path / file_path
            if full_path.exists():
                return full_path.read_text(encoding="utf-8")
            return None
        except Exception:
            return None
    
    @staticmethod
    def clean_workspace(project_name: str) -> bool:
        """Clean build artifacts from workspace"""
        try:
            workspace_path = WorkspaceManager._get_workspace_path(project_name)
            build_dir = workspace_path / "build"
            if build_dir.exists():
                import shutil
                shutil.rmtree(build_dir)
            return True
        except Exception:
            return False


class LeoBuilder:
    """Handles Leo code compilation"""
    
    @staticmethod
    def build_project(project_name: str, timeout: int = 60) -> BuildResult:
        """Compile a Leo project"""
        start_time = time.time()
        
        try:
            workspace_path = WorkspaceManager._get_workspace_path(project_name)
            
            result = subprocess.run(
                ["leo", "build"],
                cwd=workspace_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            build_time = time.time() - start_time
            
            # Parse output for errors and warnings
            errors = []
            warnings = []
            
            if result.stderr:
                for line in result.stderr.splitlines():
                    if "error" in line.lower():
                        errors.append(line)
                    elif "warning" in line.lower():
                        warnings.append(line)
            
            if result.returncode == 0:
                # Check for output files
                build_dir = workspace_path / "build"
                output_files = []
                if build_dir.exists():
                    output_files = [str(f.relative_to(build_dir)) 
                                  for f in build_dir.rglob("*") if f.is_file()]
                
                return BuildResult(
                    status=CompilationStatus.SUCCESS,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    warnings=warnings,
                    errors=errors,
                    success=True,
                    build_time=build_time,
                    output_files=output_files
                )
            else:
                return BuildResult(
                    status=CompilationStatus.ERROR,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    warnings=warnings,
                    errors=errors,
                    success=False,
                    build_time=build_time
                )
                
        except subprocess.TimeoutExpired:
            return BuildResult(
                status=CompilationStatus.TIMEOUT,
                errors=[f"Build timeout after {timeout} seconds"],
                success=False,
                build_time=timeout
            )
        except FileNotFoundError:
            return BuildResult(
                status=CompilationStatus.UNKNOWN,
                errors=["Leo CLI not found. Please install Leo first."],
                success=False,
                build_time=time.time() - start_time
            )
        except Exception as e:
            return BuildResult(
                status=CompilationStatus.UNKNOWN,
                errors=[f"Unexpected error: {str(e)}"],
                success=False,
                build_time=time.time() - start_time
            )
    
    @staticmethod
    def parse_error_details(stderr: str) -> List[dict]:
        """Parse compilation errors for detailed information"""
        errors = []
        current_error = None
        
        for line in stderr.splitlines():
            if "error:" in line:
                if current_error:
                    errors.append(current_error)
                current_error = {
                    "message": line.split("error:", 1)[1].strip(),
                    "location": "",
                    "suggestion": ""
                }
            elif "-->" in line and current_error:
                current_error["location"] = line.strip()
            elif "help:" in line and current_error:
                current_error["suggestion"] = line.split("help:", 1)[1].strip()
        
        if current_error:
            errors.append(current_error)
        
        return errors 