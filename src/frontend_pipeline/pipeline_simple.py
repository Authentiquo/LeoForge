"""
Simplified Frontend Architecture Pipeline
Generates beautiful React frontends without AI agents
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .contract_analyzer import ContractAnalyzer, ContractInfo
from .frontend_generator import FrontendGenerator


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleFrontendArchitect:
    """Simplified Frontend Architect that generates modern frontends without AI agents"""
    
    def __init__(self, output_dir: str = "generated_frontends"):
        self.output_dir = output_dir
        self.analyzer = ContractAnalyzer()
        self.specs = {}
    
    def build_frontend_project(self, contract_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Build complete frontend project"""
        
        logger.info("🏗️  Starting Frontend Architecture Process...")
        
        try:
            # Step 1: Analyze contract
            logger.info("📊 Step 1: Analyzing smart contract...")
            with open(contract_path, 'r') as f:
                contract_content = f.read()
            
            contract_info = self.analyzer.analyze(contract_content)
            
            if not project_name:
                project_name = Path(contract_path).stem.replace('.aleo', '')
            
            # Step 2: Create project specifications
            logger.info("📋 Step 2: Creating project specifications...")
            specs = self._create_project_specs(contract_info)
            
            # Step 3: Build frontend
            logger.info("🔨 Step 3: Building frontend pages...")
            frontend_path = self._build_complete_frontend(contract_info, project_name, specs)
            
            # Step 4: Generate report
            logger.info("📊 Step 4: Generating architect report...")
            report = self._generate_report(contract_info, specs, frontend_path)
            
            logger.info("✨ Frontend project completed successfully!")
            logger.info(f"📁 Project location: {frontend_path}")
            
            return {
                'success': True,
                'frontend_path': frontend_path,
                'specifications': specs,
                'report': report
            }
            
        except Exception as e:
            logger.error(f"❌ Error in frontend architecture: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_project_specs(self, contract_info: ContractInfo) -> Dict[str, Any]:
        """Create project specifications based on contract analysis"""
        
        # Extract features from contract
        features = []
        for transition in contract_info.transitions:
            features.append({
                'name': transition.name.replace('_', ' ').title(),
                'description': f"Execute {transition.name} operation",
                'type': self._categorize_transition(transition.name)
            })
        
        # Define pages based on contract
        pages = self._define_pages(contract_info)
        
        specs = {
            'project_name': contract_info.program_name,
            'overview': f"Modern web application for {contract_info.program_name} smart contract",
            'features': features,
            'pages': pages,
            'design_system': {
                'colors': {
                    'primary': '#0055FF',
                    'secondary': '#00D4FF',
                    'accent': '#FF0099',
                    'dark': '#0A0E27'
                },
                'fonts': {
                    'heading': 'Inter',
                    'body': 'Inter',
                    'mono': 'JetBrains Mono'
                }
            }
        }
        
        self.specs = specs
        return specs
    
    def _categorize_transition(self, name: str) -> str:
        """Categorize transition by type"""
        name_lower = name.lower()
        if any(keyword in name_lower for keyword in ['mint', 'burn', 'transfer', 'token']):
            return 'token_operation'
        elif any(keyword in name_lower for keyword in ['create', 'register', 'initialize']):
            return 'initialization'
        elif any(keyword in name_lower for keyword in ['admin', 'freeze', 'pause']):
            return 'admin_operation'
        elif any(keyword in name_lower for keyword in ['deposit', 'withdraw', 'stake']):
            return 'financial_operation'
        else:
            return 'general_operation'
    
    def _define_pages(self, contract_info: ContractInfo) -> List[Dict[str, Any]]:
        """Define pages based on contract analysis"""
        pages = [
            {
                'name': 'Landing Page',
                'route': '/',
                'component': 'LandingPage',
                'purpose': 'Welcome users with hero section'
            }
        ]
        
        # Group transitions by category
        categories = {}
        for transition in contract_info.transitions:
            category = self._categorize_transition(transition.name)
            if category not in categories:
                categories[category] = []
            categories[category].append(transition)
        
        # Create pages for categories
        category_names = {
            'token_operation': 'Token Management',
            'initialization': 'Setup',
            'admin_operation': 'Admin',
            'financial_operation': 'Finance',
            'general_operation': 'Operations'
        }
        
        for category, transitions in categories.items():
            page_name = category_names.get(category, 'Operations')
            pages.append({
                'name': page_name,
                'route': f'/{category.replace("_", "-")}',
                'component': f'{page_name.replace(" ", "")}Page',
                'purpose': f'Manage {page_name.lower()}',
                'transitions': [t.name for t in transitions]
            })
        
        # Add dashboard if mappings exist
        if contract_info.mappings:
            pages.append({
                'name': 'Dashboard',
                'route': '/dashboard',
                'component': 'Dashboard',
                'purpose': 'Data visualization'
            })
        
        return pages
    
    def _build_complete_frontend(self, contract_info: ContractInfo, project_name: str, specs: Dict[str, Any]) -> str:
        """Build the complete frontend project"""
        
        frontend_path = os.path.join(self.output_dir, project_name)
        os.makedirs(frontend_path, exist_ok=True)
        
        # Use the existing FrontendGenerator as base
        generator = FrontendGenerator(self.output_dir)
        
        # Generate base structure
        generator.generate(contract_info, project_name)
        
        # Enhance with modern features
        self._enhance_with_typescript(frontend_path)
        self._add_modern_components(frontend_path, specs)
        self._add_beautiful_styles(frontend_path)
        
        return frontend_path
    
    def _enhance_with_typescript(self, frontend_path: str):
        """Add TypeScript configuration"""
        
        # Update package.json with TypeScript dependencies
        package_path = os.path.join(frontend_path, 'package.json')
        if os.path.exists(package_path):
            with open(package_path, 'r') as f:
                package = json.load(f)
            
            # Add TypeScript dependencies
            package['dependencies'].update({
                "typescript": "^4.9.5",
                "@types/react": "^18.2.15",
                "@types/react-dom": "^18.2.7",
                "@types/node": "^16.18.39"
            })
            
            with open(package_path, 'w') as f:
                json.dump(package, f, indent=2)
        
        # Add tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noFallthroughCasesInSwitch": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx"
            },
            "include": ["src"]
        }
        
        with open(os.path.join(frontend_path, 'tsconfig.json'), 'w') as f:
            json.dump(tsconfig, f, indent=2)
    
    def _add_modern_components(self, frontend_path: str, specs: Dict[str, Any]):
        """Add modern UI components"""
        
        # Create a beautiful loading component
        loading_component = '''import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-primary-200 rounded-full"></div>
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-primary-500 rounded-full border-t-transparent animate-spin"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;'''
        
        components_dir = os.path.join(frontend_path, 'src', 'components')
        with open(os.path.join(components_dir, 'LoadingSpinner.js'), 'w') as f:
            f.write(loading_component)
        
        # Create a beautiful card component
        card_component = '''import React from 'react';

const Card = ({ children, className = '' }) => {
  return (
    <div className={`bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 ${className}`}>
      {children}
    </div>
  );
};

export default Card;'''
        
        with open(os.path.join(components_dir, 'Card.js'), 'w') as f:
            f.write(card_component)
    
    def _add_beautiful_styles(self, frontend_path: str):
        """Add beautiful modern styles"""
        
        # Enhanced global styles
        enhanced_styles = '''/* Modern Variables */
:root {
  --primary: #0055FF;
  --secondary: #00D4FF;
  --accent: #FF0099;
  --dark: #0A0E27;
  --light: #F7F9FF;
}

/* Animations */
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Gradient Backgrounds */
.gradient-bg {
  background: linear-gradient(-45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

/* Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Hover Effects */
.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--dark);
}

::-webkit-scrollbar-thumb {
  background: var(--primary);
  border-radius: 4px;
}

/* Beautiful Buttons */
.btn-gradient {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 85, 255, 0.3);
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 85, 255, 0.4);
}'''
        
        styles_dir = os.path.join(frontend_path, 'src', 'styles')
        
        # Append to existing App.css
        app_css_path = os.path.join(styles_dir, 'App.css')
        if os.path.exists(app_css_path):
            with open(app_css_path, 'a') as f:
                f.write('\n\n' + enhanced_styles)
    
    def _generate_report(self, contract_info: ContractInfo, specs: Dict[str, Any], frontend_path: str) -> Dict[str, Any]:
        """Generate architect report"""
        
        report = {
            'project_name': contract_info.program_name,
            'specifications': {
                'pages': len(specs['pages']),
                'features': len(specs['features']),
                'design': 'Modern with glassmorphism'
            },
            'files_generated': {
                'components': len(os.listdir(os.path.join(frontend_path, 'src', 'components'))),
                'pages': len(os.listdir(os.path.join(frontend_path, 'src', 'pages'))),
                'styles': len(os.listdir(os.path.join(frontend_path, 'src', 'styles')))
            },
            'next_steps': [
                f'cd {frontend_path}',
                'npm install',
                'npm start'
            ]
        }
        
        # Save report
        with open(os.path.join(frontend_path, 'architect_report.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Create README
        readme = f'''# {contract_info.program_name.replace("_", " ").title()} Frontend

## Overview
Modern frontend for the {contract_info.program_name} Aleo smart contract.

## Features
- 🎨 Beautiful modern UI
- ⚡ React 18
- 💎 TypeScript support
- 🌈 Glassmorphism design
- 📱 Fully responsive

## Quick Start
```bash
npm install
npm start
```

## Pages
{chr(10).join([f"- **{p['name']}** ({p['route']}): {p['purpose']}" for p in specs['pages']])}

---
Made with ❤️ by AleoForge
'''
        
        with open(os.path.join(frontend_path, 'README.md'), 'w') as f:
            f.write(readme)
        
        return report 