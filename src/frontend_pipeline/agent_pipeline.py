"""
Agent-based Frontend Pipeline for Aleo Smart Contracts
Dynamic frontend generation with error detection and fixing
"""

import os
import json
import logging
import subprocess
import time
import asyncio
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path

# OpenAI Agents imports
try:
    from agents import Agent, AgentContext, AgentFunction, AgentResponse
    from agents.manager import AgentManager
except ImportError:
    # For development/testing
    class Agent:
        def __init__(self, name: str, model: str = "gpt-4", instructions: str = "", tools: List = None):
            self.name = name
            self.model = model
            self.instructions = instructions
            self.tools = tools or []

from .contract_analyzer import ContractAnalyzer, ContractInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Tool definitions using OpenAI Agent format
def analyze_contract(contract_path: str) -> Dict[str, Any]:
    """Analyze an Aleo smart contract to extract its structure and functionality"""
    try:
        analyzer = ContractAnalyzer()
        with open(contract_path, 'r') as f:
            contract_content = f.read()
        
        contract_info = analyzer.analyze(contract_content)
        
        return {
            'success': True,
            'program_name': contract_info.program_name,
            'transitions': [
                {
                    'name': t.name, 
                    'parameters': t.parameters, 
                    'is_async': t.is_async,
                    'returns': t.returns
                }
                for t in contract_info.transitions
            ],
            'mappings': [
                {'name': m.name, 'key_type': m.key_type, 'value_type': m.value_type}
                for m in contract_info.mappings
            ],
            'records': [
                {'name': r.name, 'fields': r.fields}
                for r in contract_info.records
            ],
            'summary': f"Contract '{contract_info.program_name}' with {len(contract_info.transitions)} transitions"
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def create_file(file_path: str, content: str, description: str = "") -> Dict[str, Any]:
    """Create or update a file with the given content"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created file: {file_path} - {description}")
        return {
            'success': True, 
            'file_path': file_path,
            'description': description
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def check_project_errors(project_path: str) -> Dict[str, Any]:
    """Check a React project for build/runtime errors without fully starting it"""
    try:
        # First check if package.json exists
        package_json_path = os.path.join(project_path, 'package.json')
        if not os.path.exists(package_json_path):
            return {
                'success': False,
                'has_errors': True,
                'errors': ['package.json not found']
            }
        
        # Run a build to check for errors
        logger.info("Running build check...")
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            # Parse errors from output
            errors = []
            output = result.stdout + result.stderr
            
            # Extract error messages
            for line in output.split('\n'):
                if 'error' in line.lower() and line.strip():
                    errors.append(line.strip())
            
            return {
                'success': True,
                'has_errors': True,
                'errors': errors[:10],  # Limit to first 10 errors
                'raw_output': output[:2000]  # First 2000 chars
            }
        
        return {
            'success': True,
            'has_errors': False,
            'message': 'Build successful, no errors found'
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Build check timed out'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fix_file_error(file_path: str, error_description: str, fix_code: str) -> Dict[str, Any]:
    """Fix an error in a specific file by replacing its content"""
    try:
        # Write the fixed code
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fix_code)
        
        logger.info(f"Fixed error in {file_path}: {error_description}")
        return {
            'success': True,
            'file_path': file_path,
            'error_fixed': error_description
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def list_project_files(project_path: str, extensions: List[str] = None) -> Dict[str, Any]:
    """List all files in a project with specific extensions"""
    try:
        if extensions is None:
            extensions = ['.tsx', '.ts', '.jsx', '.js', '.css', '.json']
        
        files = []
        for root, _, filenames in os.walk(project_path):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, project_path)
                    files.append(relative_path)
        
        return {
            'success': True,
            'files': sorted(files),
            'count': len(files)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


class DAppAgentPipeline:
    """Modern agent pipeline for generating dApp frontends"""
    
    def __init__(self, output_dir: str = "generated_frontends"):
        self.output_dir = output_dir
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup specialized agents with their tools"""
        
        # Smart Contract Analyzer Agent
        self.analyzer_agent = Agent(
            name="Smart Contract Analyzer",
            model="gpt-4",
            instructions="""You are an expert in analyzing Aleo smart contracts.
            
            Your responsibilities:
            1. Analyze the contract structure and identify all transitions, mappings, and records
            2. Understand the business logic and purpose of the contract
            3. Determine what kind of dApp this is (DeFi, NFT, Gaming, etc.)
            4. Identify the key user interactions needed
            
            Always provide clear, structured analysis focusing on what frontend features are needed.""",
            tools=[analyze_contract]
        )
        
        # Frontend Architect Agent
        self.architect_agent = Agent(
            name="Frontend Architect",
            model="gpt-4",
            instructions="""You are a senior frontend architect specializing in Web3 dApps.
            
            Your responsibilities:
            1. Design a simple, clean architecture for the dApp
            2. Plan the minimal set of pages needed
            3. Structure components logically
            4. Use React + TypeScript + Tailwind CSS
            
            Design principles:
            - Keep it simple and functional
            - Mobile-first responsive design
            - Clean, modern UI
            - Focus on user experience
            
            IMPORTANT: Always include a footer component with "Made with ❤️ by AleoForge" """,
            tools=[create_file, list_project_files]
        )
        
        # React Developer Agent
        self.developer_agent = Agent(
            name="React Developer",
            model="gpt-4",
            instructions="""You are an expert React developer building Web3 frontends.
            
            Your responsibilities:
            1. Write clean React components with TypeScript
            2. Use Tailwind CSS for styling
            3. Create forms for smart contract interactions
            4. Handle loading states and errors properly
            
            Technical requirements:
            - React 18 with functional components and hooks
            - TypeScript for all components
            - Tailwind CSS classes only (no custom CSS)
            - Proper prop types and interfaces
            - Mock contract calls with console.log for now
            
            Code style:
            - Clear, readable code
            - Proper component organization
            - Reusable components where appropriate""",
            tools=[create_file, list_project_files]
        )
        
        # Error Detective Agent
        self.detective_agent = Agent(
            name="Error Detective",
            model="gpt-4",
            instructions="""You are a debugging expert for React/TypeScript projects.
            
            Your responsibilities:
            1. Identify build and compilation errors
            2. Locate the exact files and lines causing issues
            3. Understand TypeScript errors
            4. Diagnose missing imports or dependencies
            
            Focus on:
            - Clear error identification
            - Root cause analysis
            - Specific file locations
            - Actionable solutions""",
            tools=[check_project_errors, list_project_files]
        )
        
        # Code Fixer Agent
        self.fixer_agent = Agent(
            name="Code Fixer",
            model="gpt-4",
            instructions="""You are a code fixing specialist for React/TypeScript projects.
            
            Your responsibilities:
            1. Fix compilation and runtime errors
            2. Add missing imports
            3. Correct TypeScript type errors
            4. Ensure all components work together
            
            Rules:
            - Fix one error at a time
            - Preserve existing functionality
            - Write complete, working code
            - Test that fixes resolve the issue""",
            tools=[fix_file_error, create_file, check_project_errors]
        )
    
    async def generate_frontend(self, contract_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Generate a complete dApp frontend using the agent pipeline"""
        
        logger.info("🚀 Starting dApp Frontend Generation")
        
        try:
            # Determine project name
            if not project_name:
                project_name = Path(contract_path).stem.replace('.aleo', '')
            
            project_path = os.path.join(self.output_dir, project_name)
            
            # Step 1: Analyze the contract
            logger.info("📊 Step 1: Analyzing smart contract...")
            analysis_result = await self._run_agent(
                self.analyzer_agent,
                f"Analyze the smart contract at: {contract_path}"
            )
            
            # Step 2: Design the architecture
            logger.info("🏗️ Step 2: Designing frontend architecture...")
            architecture_prompt = f"""
            Based on the contract analysis, design a simple frontend architecture.
            
            Project path: {project_path}
            Contract analysis: {analysis_result}
            
            Create:
            1. package.json with all necessary dependencies
            2. tsconfig.json for TypeScript
            3. tailwind.config.js for Tailwind CSS
            4. Basic project structure
            
            Keep it minimal but functional.
            """
            
            await self._run_agent(self.architect_agent, architecture_prompt)
            
            # Step 3: Generate core components
            logger.info("⚛️ Step 3: Generating React components...")
            components_prompt = f"""
            Generate the core React components for this dApp.
            
            Project path: {project_path}
            
            Create:
            1. App.tsx - Main app component with routing
            2. Layout components (Header, Footer with "Made with ❤️ by AleoForge")
            3. Home page component
            4. Contract interaction components based on the transitions
            
            Use TypeScript and Tailwind CSS for all components.
            """
            
            await self._run_agent(self.developer_agent, components_prompt)
            
            # Step 4: Check for errors and fix them
            logger.info("🔍 Step 4: Checking for errors...")
            error_check_result = await self._run_agent(
                self.detective_agent,
                f"Check the project at {project_path} for any build errors"
            )
            
            # Step 5: Fix any errors found
            if "has_errors" in str(error_check_result) and "True" in str(error_check_result):
                logger.info("🔧 Step 5: Fixing errors...")
                fix_prompt = f"""
                Fix the errors found in the project.
                
                Project path: {project_path}
                Errors: {error_check_result}
                
                Fix each error one by one, ensuring the project builds successfully.
                """
                
                await self._run_agent(self.fixer_agent, fix_prompt)
                
                # Verify fixes
                logger.info("✅ Verifying fixes...")
                final_check = await self._run_agent(
                    self.detective_agent,
                    f"Verify the project at {project_path} now builds without errors"
                )
            
            logger.info("✨ Frontend generation completed!")
            
            return {
                'success': True,
                'project_path': project_path,
                'project_name': project_name,
                'message': f'dApp frontend generated at {project_path}'
            }
            
        except Exception as e:
            logger.error(f"❌ Error in pipeline: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _run_agent(self, agent: Agent, prompt: str) -> Any:
        """Run an agent with a prompt"""
        try:
            # For now, simulate agent execution
            # In production, this would use the actual OpenAI Agents SDK
            logger.info(f"Running {agent.name}: {prompt[:100]}...")
            
            # Simulate tool execution based on agent
            if agent.name == "Smart Contract Analyzer" and analyze_contract in agent.tools:
                # Extract contract path from prompt
                import re
                match = re.search(r'at:\s*(.+\.aleo)', prompt)
                if match:
                    return analyze_contract(match.group(1))
            
            # For other agents, we'd implement similar logic
            # This is a simplified version for demonstration
            
            return {'status': 'completed', 'agent': agent.name}
            
        except Exception as e:
            logger.error(f"Error running agent {agent.name}: {str(e)}")
            raise
    
    def generate_frontend_sync(self, contract_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous wrapper for generate_frontend"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.generate_frontend(contract_path, project_name))
        finally:
            loop.close()


# Main entry point
def generate_dapp_frontend(contract_path: str, output_dir: str = "generated_frontends") -> Dict[str, Any]:
    """Generate a dApp frontend from an Aleo smart contract using agents"""
    pipeline = DAppAgentPipeline(output_dir)
    return pipeline.generate_frontend_sync(contract_path) 