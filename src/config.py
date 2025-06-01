"""
Configuration module for LeoForge
Manages environment variables and application settings
"""
import os
from typing import Optional
from pydantic import BaseModel, Field


class LeoForgeConfig(BaseModel):
    """Configuration settings for LeoForge"""
    
    # API Keys
    anthropic_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"),
        description="Anthropic API key for Claude models"
    )
    
    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key for GPT models"
    )
    
    deepseek_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("DEEPSEEK_API_KEY"),
        description="DeepSeek API key for DeepSeek models"
    )
    
    # Admin configuration
    admin_address: str = Field(
        default_factory=lambda: os.getenv(
            "ADMIN_ADDRESS",
            "aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0"
        ),
        description="Default admin address for Leo blockchain operations"
    )
    
    # Model configurations
    default_architect_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Default model for the Architect agent"
    )
    
    default_generator_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Default model for the Code Generator agent"
    )
    
    default_evaluator_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Default model for the Code Evaluator agent"
    )
    
    # Generation settings
    max_iterations: int = Field(
        default=5,
        description="Maximum iterations for code generation"
    )
    
    build_timeout: int = Field(
        default=30,
        description="Timeout for build operations in seconds"
    )
    
    def validate_api_keys(self) -> bool:
        """Validate that at least one API key is configured"""
        return bool(self.anthropic_api_key or self.openai_api_key)
    
    def get_admin_address(self) -> str:
        """Get the configured admin address"""
        return self.admin_address
    
    def is_valid_aleo_address(self, address: str) -> bool:
        """Validate if an address is a valid Aleo address format"""
        return (
            address.startswith("aleo1") and 
            len(address) == 63 and 
            all(c in "0123456789abcdefghijklmnopqrstuvwxyz" for c in address[5:])
        )


# Global configuration instance
config = LeoForgeConfig()


def get_config() -> LeoForgeConfig:
    """Get the global configuration instance"""
    return config


def update_admin_address(new_address: str) -> bool:
    """Update the admin address with validation"""
    global config
    if config.is_valid_aleo_address(new_address):
        config.admin_address = new_address
        return True
    return False 