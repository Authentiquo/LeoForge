import os
import re
from rich.console import Console
from ..tools.leo_tools import execute_command, save_leo_code

console = Console()

def create_composite_project(main_project, dependencies=None):
    """Create a composite project that imports other Leo programs."""
    if not dependencies:
        dependencies = []
    
    # Create the main project
    console.print(f"[bold green]Creating composite project: {main_project}[/bold green]")
    result = execute_command(f"leo new {main_project}")
    
    if not result["success"]:
        console.print(f"[bold red]Failed to create main project: {result['stderr']}[/bold red]")
        return False
    
    # Update the program.json to include imports
    update_program_imports(main_project, dependencies)
    
    # Link the dependent projects in the imports directory
    for dep in dependencies:
        link_dependency(main_project, dep)
    
    return True

def update_program_imports(project_name, dependencies):
    """Update the program.json file to include imports from dependencies."""
    program_json_path = f"{project_name}/program.json"
    
    try:
        with open(program_json_path, 'r') as file:
            content = file.read()
        
        # Simple string replacement to add imports
        # In a real implementation, use proper JSON parsing
        import_section = '"imports": {'
        for dep in dependencies:
            dep_name = os.path.basename(dep)
            import_section += f'"{dep_name}": "../{dep}/build/{dep_name}.aleo",'
        
        # Remove trailing comma if there are dependencies
        if dependencies:
            import_section = import_section[:-1]
        
        import_section += '}'
        
        # Replace or add imports section
        if '"imports": {}' in content:
            content = content.replace('"imports": {}', import_section)
        else:
            # Add imports section after program section
            pattern = r'("program": "[^"]+")'
            content = re.sub(pattern, r'\1,\n  ' + import_section, content)
        
        with open(program_json_path, 'w') as file:
            file.write(content)
        
        console.print(f"[green]Updated program.json with imports in {project_name}[/green]")
        return True
    
    except Exception as e:
        console.print(f"[bold red]Failed to update program imports: {str(e)}[/bold red]")
        return False

def link_dependency(main_project, dependency):
    """Set up the dependency link for the main project."""
    try:
        # Ensure the imports directory exists
        imports_dir = f"{main_project}/imports"
        os.makedirs(imports_dir, exist_ok=True)
        
        # Create a symbolic link or copy the build artifacts
        dep_name = os.path.basename(dependency)
        source = f"../{dependency}/build/{dep_name}.aleo"
        target = f"{imports_dir}/{dep_name}.aleo"
        
        # Try to create a symbolic link first
        try:
            if os.path.exists(target):
                os.remove(target)
            os.symlink(source, target)
        except:
            # If symlink fails, copy the file instead
            if os.path.exists(source):
                with open(source, 'r') as src_file:
                    content = src_file.read()
                with open(target, 'w') as tgt_file:
                    tgt_file.write(content)
        
        console.print(f"[green]Linked dependency {dep_name} to {main_project}[/green]")
        return True
    
    except Exception as e:
        console.print(f"[bold red]Failed to link dependency: {str(e)}[/bold red]")
        return False

def add_import_to_code(main_code, dependency_name):
    """Add import statement to the main code."""
    dep_basename = os.path.basename(dependency_name)
    import_statement = f"import {dep_basename}.aleo;\n\n"
    
    # If there's already a program declaration, add import before it
    if "program " in main_code:
        pattern = r'(program [^{]+\{)'
        main_code = re.sub(pattern, f"{import_statement}\\1", main_code)
    else:
        main_code = import_statement + main_code
    
    return main_code 