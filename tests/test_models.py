"""
Tests for LeoForge data models
"""
import pytest
from datetime import datetime
from src.models import (
    ProjectType, UserQuery, ArchitectureDesign, 
    CodeRequirements, GeneratedCode, EvaluationResult,
    CompilationStatus, BuildResult
)


def test_project_type_enum():
    """Test ProjectType enum values"""
    assert ProjectType.TOKEN.value == "token"
    assert ProjectType.NFT.value == "nft"
    assert ProjectType.DEFI.value == "defi"
    assert len(ProjectType) == 6


def test_user_query_creation():
    """Test UserQuery model creation"""
    query = UserQuery(
        query="Create a simple token",
        project_type=ProjectType.TOKEN,
        constraints=["Must be gas efficient", "Support batch transfers"]
    )
    
    assert query.query == "Create a simple token"
    assert query.project_type == ProjectType.TOKEN
    assert len(query.constraints) == 2
    assert isinstance(query.timestamp, datetime)


def test_architecture_design():
    """Test ArchitectureDesign model"""
    design = ArchitectureDesign(
        project_name="my_token",
        project_type=ProjectType.TOKEN,
        description="A simple token implementation",
        features=["mint", "transfer", "burn"],
        technical_requirements=["ERC20 compatible"],
        data_structures=["Token: record with owner and amount"],
        transitions=["mint: (address, u64) -> Token"],
        security_considerations=["Check for overflow"],
        admin_features=["Admin can pause contract"],
        requires_admin=True
    )
    
    assert design.project_name == "my_token"
    assert len(design.features) == 3
    assert "Token: record with owner and amount" in design.data_structures
    assert "mint: (address, u64) -> Token" in design.transitions
    assert design.requires_admin is True


def test_evaluation_result():
    """Test EvaluationResult model"""
    result = EvaluationResult(
        is_complete=True,
        has_errors=False,
        missing_features=["burn function"],
        improvements=["Add input validation", "Optimize loops"],
        security_issues=[],
        optimization_suggestions=["Use batch operations"],
        score=85.5,
        needs_iteration=True
    )
    
    assert result.is_complete is True
    assert result.has_errors is False
    assert result.score == 85.5
    assert len(result.improvements) == 2
    assert result.needs_iteration is True


def test_build_result():
    """Test BuildResult model"""
    result = BuildResult(
        status=CompilationStatus.SUCCESS,
        stdout="Build successful",
        stderr="",
        warnings=["Unused variable"],
        errors=[],
        success=True,
        build_time=2.5,
        output_files=["main.aleo", "main.prover", "main.verifier"]
    )
    
    assert result.status == CompilationStatus.SUCCESS
    assert result.success is True
    assert result.build_time == 2.5
    assert len(result.output_files) == 3


def test_generated_code():
    """Test GeneratedCode model"""
    code = GeneratedCode(
        code="program token.aleo { ... }",
        language="leo",
        file_path="src/main.leo",
        imports=["std.aleo"],
        exports=["Token", "mint", "transfer"],
        warnings=["Consider adding access control"]
    )
    
    assert code.language == "leo"
    assert code.file_path == "src/main.leo"
    assert len(code.imports) == 1
    assert len(code.exports) == 3
    assert isinstance(code.generation_time, datetime)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 