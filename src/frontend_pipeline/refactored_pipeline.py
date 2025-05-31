"""
Refactored Frontend Pipeline for Aleo Smart Contracts
Progressive generation with real-time error detection and fixing
"""

import os
import json
import logging
import subprocess
import time
from typing import Dict, Any, Optional, List
from pathlib import Path

# Import our tools
from .contract_analyzer import ContractAnalyzer
from .openai_agent_tools import (
    create_project_structure,
    install_dependencies,
    parse_build_errors,
    generate_app_component,
    generate_header_component,
    generate_footer_component,
    generate_home_page
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProgressiveFrontendPipeline:
    """Pipeline that generates frontend progressively and fixes errors on the fly"""
    
    def __init__(self, output_dir: str = "generated_frontends"):
        self.output_dir = output_dir
        self.analyzer = ContractAnalyzer()
        self.current_project = None
        self.contract_info = None
    
    def generate_frontend(self, contract_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Generate a dApp frontend progressively"""
        
        logger.info("🚀 Starting Progressive Frontend Generation")
        
        try:
            # Step 1: Analyze the contract
            logger.info("📊 Step 1: Analyzing smart contract...")
            with open(contract_path, 'r') as f:
                contract_content = f.read()
            
            self.contract_info = self.analyzer.analyze(contract_content)
            
            if not project_name:
                project_name = self.contract_info.program_name or Path(contract_path).stem
            
            self.current_project = os.path.join(self.output_dir, project_name)
            
            # Step 2: Create basic project structure
            logger.info("🏗️ Step 2: Creating project structure...")
            structure_result = create_project_structure(self.current_project)
            if not structure_result['success']:
                return structure_result
            
            # Step 3: Generate core components page by page
            logger.info("📄 Step 3: Generating components progressively...")
            self._generate_core_components()
            
            # Step 4: Install dependencies
            logger.info("📦 Step 4: Installing dependencies...")
            install_result = install_dependencies(self.current_project)
            if not install_result['success']:
                logger.warning(f"Dependency installation failed: {install_result['error']}")
            
            # Step 5: Check and fix errors
            logger.info("🔍 Step 5: Checking for errors...")
            error_check = self._check_for_errors()
            
            if error_check['has_errors']:
                logger.info("🔧 Step 6: Fixing errors...")
                self._fix_errors(error_check['errors'])
                
                # Verify fixes
                final_check = self._check_for_errors()
                if final_check['has_errors']:
                    logger.warning("Some errors remain after fixing attempt")
                else:
                    logger.info("✅ All errors fixed!")
            else:
                logger.info("✅ No errors found!")
            
            # Step 7: Generate additional pages based on contract
            logger.info("📑 Step 7: Generating contract-specific pages...")
            self._generate_contract_pages()
            
            logger.info("✨ Frontend generation completed!")
            
            return {
                'success': True,
                'project_path': self.current_project,
                'project_name': project_name,
                'contract_name': self.contract_info.program_name,
                'transitions': [t.name for t in self.contract_info.transitions],
                'message': f'dApp frontend generated at {self.current_project}'
            }
            
        except Exception as e:
            logger.error(f"❌ Error in pipeline: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_core_components(self):
        """Generate core React components"""
        
        # Generate App.tsx
        logger.info("  - Generating App.tsx...")
        app_content = generate_app_component(
            self.contract_info.program_name,
            [{'name': t.name} for t in self.contract_info.transitions]
        )
        self._write_file('src/App.tsx', app_content)
        
        # Generate Header component
        logger.info("  - Generating Header component...")
        header_content = generate_header_component(self.contract_info.program_name)
        self._write_file('src/components/Header.tsx', header_content)
        
        # Generate Footer component with AleoForge branding
        logger.info("  - Generating Footer component...")
        footer_content = generate_footer_component()
        self._write_file('src/components/Footer.tsx', footer_content)
        
        # Generate Home page
        logger.info("  - Generating Home page...")
        home_content = generate_home_page()
        self._write_file('src/pages/HomePage.tsx', home_content)
    
    def _generate_contract_pages(self):
        """Generate pages for contract interactions"""
        
        # Group transitions by category
        categories = {}
        for transition in self.contract_info.transitions:
            category = self._categorize_transition(transition.name)
            if category not in categories:
                categories[category] = []
            categories[category].append(transition)
        
        # Generate a page for each category
        for category, transitions in categories.items():
            page_name = category.replace('_', ' ').title().replace(' ', '') + 'Page'
            logger.info(f"  - Generating {page_name}...")
            
            page_content = self._generate_operation_page(category, transitions)
            self._write_file(f'src/pages/{page_name}.tsx', page_content)
    
    def _generate_operation_page(self, category: str, transitions: List[Any]) -> str:
        """Generate an operation page for a category of transitions"""
        
        page_name = category.replace('_', ' ').title().replace(' ', '') + 'Page'
        
        # Generate form fields for each transition
        forms = []
        for transition in transitions:
            form = self._generate_transition_form(transition)
            forms.append(form)
        
        forms_jsx = '\n\n'.join(forms)
        
        return f"""import React, {{ useState }} from 'react'

const {page_name}: React.FC = () => {{
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<string | null>(null)
  
  const handleSubmit = async (transitionName: string, formData: any) => {{
    setLoading(true)
    setResult(null)
    
    try {{
      // Mock contract call
      console.log(`Calling ${{transitionName}} with data:`, formData)
      
      // Simulate async operation
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setResult(`Successfully called ${{transitionName}}`)
    }} catch (error) {{
      setResult(`Error: ${{error}}`)
    }} finally {{
      setLoading(false)
    }}
  }}
  
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8 text-aleo-dark">
        {category.replace('_', ' ').title()}
      </h1>
      
      <div className="space-y-8">
{forms_jsx}
      </div>
      
      {{loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg">
            <p className="text-lg">Processing transaction...</p>
          </div>
        </div>
      )}}
      
      {{result && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <p className="font-mono text-sm">{{result}}</p>
        </div>
      )}}
    </div>
  )
}}

export default {page_name}"""
    
    def _generate_transition_form(self, transition: Any) -> str:
        """Generate a form for a single transition"""
        
        # Generate input fields
        fields = []
        for param in transition.parameters:
            field = f"""
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {param['name']}
            </label>
            <input
              type="text"
              name="{param['name']}"
              placeholder="{param['type']}"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              required
            />
          </div>"""
            fields.append(field)
        
        fields_jsx = '\n'.join(fields) if fields else '<p className="text-gray-500">No parameters required</p>'
        
        return f"""        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">{transition.name}</h2>
          
          <form onSubmit={{(e) => {{
            e.preventDefault()
            const formData = new FormData(e.currentTarget)
            const data = Object.fromEntries(formData)
            handleSubmit('{transition.name}', data)
          }}}}>
            <div className="space-y-4">
{fields_jsx}
            </div>
            
            <button
              type="submit"
              disabled={{loading}}
              className="mt-6 w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-600 transition disabled:opacity-50"
            >
              Execute {transition.name}
            </button>
          </form>
        </div>"""
    
    def _categorize_transition(self, name: str) -> str:
        """Categorize transition by type"""
        name_lower = name.lower()
        if any(keyword in name_lower for keyword in ['mint', 'burn', 'transfer', 'token']):
            return 'token_operations'
        elif any(keyword in name_lower for keyword in ['create', 'register', 'initialize']):
            return 'initialization'
        elif any(keyword in name_lower for keyword in ['admin', 'freeze', 'pause']):
            return 'admin'
        elif any(keyword in name_lower for keyword in ['deposit', 'withdraw', 'stake']):
            return 'financial'
        else:
            return 'operations'
    
    def _write_file(self, relative_path: str, content: str):
        """Write a file relative to the project root"""
        full_path = os.path.join(self.current_project, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _check_for_errors(self) -> Dict[str, Any]:
        """Check the project for build errors"""
        try:
            # Try to build the project
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=self.current_project,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                errors = parse_build_errors(result.stdout + result.stderr)
                return {
                    'has_errors': True,
                    'errors': errors,
                    'raw_output': result.stdout + result.stderr
                }
            
            return {'has_errors': False}
            
        except subprocess.TimeoutExpired:
            return {
                'has_errors': True,
                'errors': [{'type': 'timeout', 'message': 'Build timed out'}]
            }
        except Exception as e:
            return {
                'has_errors': True,
                'errors': [{'type': 'exception', 'message': str(e)}]
            }
    
    def _fix_errors(self, errors: List[Dict[str, Any]]):
        """Attempt to fix detected errors"""
        
        for error in errors[:5]:  # Fix up to 5 errors at a time
            if error['type'] == 'typescript':
                self._fix_typescript_error(error)
            elif error['type'] == 'import':
                self._fix_import_error(error)
            elif error['type'] == 'jsx':
                self._fix_jsx_error(error)
    
    def _fix_typescript_error(self, error: Dict[str, Any]):
        """Fix TypeScript errors"""
        logger.info(f"  - Fixing TypeScript error in {error.get('file', 'unknown')}")
        
        # Common fixes
        if "Property 'contractName' does not exist" in error.get('message', ''):
            # Fix destructuring issue
            file_path = os.path.join(self.current_project, error['file'])
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Fix the destructuring syntax
                content = content.replace(
                    '({ contractName })',
                    '({ contractName }: HeaderProps)'
                )
                
                with open(file_path, 'w') as f:
                    f.write(content)
    
    def _fix_import_error(self, error: Dict[str, Any]):
        """Fix import errors"""
        logger.info(f"  - Fixing import error: {error.get('module', 'unknown')}")
        
        # Handle missing page imports
        if error.get('module', '').startswith('./pages/'):
            page_name = error['module'].split('/')[-1]
            if not page_name.endswith('.tsx'):
                page_name += '.tsx'
            
            # Generate a placeholder page if it doesn't exist
            page_path = os.path.join(self.current_project, 'src', 'pages', page_name)
            if not os.path.exists(page_path):
                placeholder = f"""import React from 'react'

const {page_name.replace('.tsx', '')}: React.FC = () => {{
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">{{page_name.replace('.tsx', '')}}</h1>
      <p>Page under construction...</p>
    </div>
  )
}}

export default {page_name.replace('.tsx', '')}"""
                
                self._write_file(f'src/pages/{page_name}', placeholder)
    
    def _fix_jsx_error(self, error: Dict[str, Any]):
        """Fix JSX errors"""
        logger.info(f"  - Fixing JSX error in {error.get('file', 'unknown')}")
        
        # Common JSX fixes would go here
        pass


# Main entry point
def generate_progressive_frontend(contract_path: str, output_dir: str = "generated_frontends") -> Dict[str, Any]:
    """Generate a dApp frontend progressively with error fixing"""
    pipeline = ProgressiveFrontendPipeline(output_dir)
    return pipeline.generate_frontend(contract_path) 