"""
Frontend Pipeline for AleoForge
Automated frontend generation from Aleo smart contracts
"""

from .contract_analyzer import ContractAnalyzer, ContractInfo
from .frontend_generator import FrontendGenerator
from .pipeline import FrontendArchitect, generate_frontend_from_contract
from .pipeline_simple import SimpleFrontendArchitect

__all__ = [
    'ContractAnalyzer',
    'ContractInfo', 
    'FrontendGenerator',
    'FrontendArchitect',
    'SimpleFrontendArchitect',
    'generate_frontend_from_contract'
]

__version__ = '0.2.0' 