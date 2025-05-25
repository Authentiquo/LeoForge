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
    
    @staticmethod
    def create_workspace(project_name: str) -> tuple[bool, str]:
        """Create a new Leo workspace"""
        workspace_path = Path(project_name).resolve()
        
        if workspace_path.exists():
            return True, str(workspace_path)
        
        try:
            result = subprocess.run(
                ["leo", "new", project_name],
                capture_output=True,
                text=True,
                check=True
            )
            return True, str(workspace_path)
        except subprocess.CalledProcessError as e:
            return False, f"Failed to create workspace: {e.stderr}"
        except FileNotFoundError:
            return False, "Leo CLI not found. Please install Leo first."
    
    @staticmethod
    def save_code(project_name: str, code: str) -> bool:
        """Save code to workspace main.leo file"""
        try:
            file_path = Path(project_name) / "src" / "main.leo"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(code, encoding="utf-8")
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def read_code(project_name: str, file_path: str = "src/main.leo") -> Optional[str]:
        """Read code from workspace"""
        try:
            full_path = Path(project_name) / file_path
            if full_path.exists():
                return full_path.read_text(encoding="utf-8")
            return None
        except Exception:
            return None
    
    @staticmethod
    def clean_workspace(project_name: str) -> bool:
        """Clean build artifacts from workspace"""
        try:
            build_dir = Path(project_name) / "build"
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
            result = subprocess.run(
                ["leo", "build"],
                cwd=Path(project_name),
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
                build_dir = Path(project_name) / "build"
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