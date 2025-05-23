import os
import subprocess
from rich.console import Console

console = Console()

def execute_command(command):
    """Execute a shell command and return the output and error."""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        stdout, stderr = process.communicate()
        return {
            "success": process.returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": process.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "return_code": -1
        }

def create_leo_project(project_name):
    """Create a new Leo project."""
    temp_project_name = f"temp_{project_name}"
    result = execute_command(f"leo new {temp_project_name}")
    
    if result["success"]:
        console.print(f"[green]Successfully created Leo project: {temp_project_name}[/green]")
        return temp_project_name
    else:
        console.print(f"[red]Failed to create Leo project: {result['stderr']}[/red]")
        return None

def save_leo_code(project_name, file_path, code_content):
    """Save generated Leo code to the project directory."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(code_content)
        console.print(f"[green]Saved Leo code to {file_path}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Failed to save Leo code: {str(e)}[/red]")
        return False

def build_leo_project(project_path):
    """Build the Leo project."""
    current_dir = os.getcwd()
    try:
        os.chdir(project_path)
        result = execute_command("leo build")
        
        if result["success"]:
            console.print(f"[green]Successfully built Leo project[/green]")
            return True
        else:
            console.print(f"[red]Failed to build Leo project: {result['stderr']}[/red]")
            return False
    finally:
        os.chdir(current_dir)

def verify_private_key(private_key):
    """Verify if the provided Aleo private key is valid."""
    # This is a simplified validation
    # In a real implementation, you should perform proper validation
    if private_key and len(private_key) > 30 and private_key.startswith("APrivateKey"):
        return True
    return False 