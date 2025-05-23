"""
Tools for Leo code generation using OpenAI Agents SDK.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from agents import FunctionTool

from .leo_tools import create_leo_project, build_leo_project, save_leo_code, verify_private_key

class ProjectInfo(BaseModel):
    """Information about a Leo project."""
    name: str = Field(..., description="The name of the Leo project")
    code: str = Field(..., description="The generated Leo code for this project")
    success: bool = Field(..., description="Whether the code generation was successful")

class VerifyCodeResult(BaseModel):
    """Result of Leo code verification."""
    is_valid: bool = Field(..., description="Whether the Leo code is valid")
    issues: List[str] = Field(default_factory=list, description="List of issues found in the code")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")

def create_project_tool(project_name: str) -> Dict[str, Any]:
    """Create a new Leo project with the given name."""
    result = create_leo_project(project_name)
    return {
        "success": bool(result),
        "project_path": result if result else None,
        "message": f"Project {project_name} created successfully" if result else f"Failed to create project {project_name}"
    }

def save_code_tool(project_name: str, code: str) -> Dict[str, Any]:
    """Save Leo code to a project file."""
    file_path = f"temp_{project_name}/src/main.leo"
    success = save_leo_code(project_name, file_path, code)
    return {
        "success": success,
        "file_path": file_path if success else None,
        "message": f"Code saved to {file_path}" if success else "Failed to save code"
    }

def build_project_tool(project_path: str) -> Dict[str, Any]:
    """Build a Leo project."""
    success = build_leo_project(project_path)
    return {
        "success": success,
        "message": "Project built successfully" if success else "Failed to build project"
    }

def verify_code_tool(code: str) -> VerifyCodeResult:
    """Verify the provided Leo code for common errors and issues."""
    # This is a placeholder - in a real implementation, you might use a Leo parser or syntax checker
    issues = []
    suggestions = []
    
    # Simple checks (these should be more sophisticated in a real implementation)
    if not code.strip():
        issues.append("Code is empty")
    
    if not "@program" in code:
        issues.append("Missing @program directive")
        suggestions.append("Add @program directive with your program ID")
    
    if "function" not in code:
        issues.append("No functions defined")
        suggestions.append("Add at least one function to your program")
    
    return VerifyCodeResult(
        is_valid=len(issues) == 0,
        issues=issues,
        suggestions=suggestions
    )

# Create function tools for the Agents SDK
create_project_tool_function = FunctionTool.from_function(
    create_project_tool,
    name="create_leo_project",
    description="Create a new Leo project with the given name"
)

save_code_tool_function = FunctionTool.from_function(
    save_code_tool,
    name="save_leo_code",
    description="Save Leo code to a project file"
)

build_project_tool_function = FunctionTool.from_function(
    build_project_tool,
    name="build_leo_project",
    description="Build a Leo project"
)

verify_code_tool_function = FunctionTool.from_function(
    verify_code_tool,
    name="verify_leo_code",
    description="Verify the provided Leo code for common errors and issues"
) 