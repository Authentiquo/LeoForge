"""
Frontend Pipeline for Aleo Smart Contracts
Generates modern dApp frontends from Aleo smart contracts using AI agents
"""

from .contract_analyzer import ContractAnalyzer, ContractInfo

# New agent-based pipelines
from .agent_pipeline import DAppAgentPipeline, generate_dapp_frontend
from .refactored_pipeline import ProgressiveFrontendPipeline, generate_progressive_frontend

__all__ = [
    # Core analyzer
    'ContractAnalyzer',
    'ContractInfo',
    # Agent-based pipeline
    'DAppAgentPipeline',
    'generate_dapp_frontend',
    # Progressive pipeline
    'ProgressiveFrontendPipeline',
    'generate_progressive_frontend'
]

# Version info
__version__ = '0.3.0' 