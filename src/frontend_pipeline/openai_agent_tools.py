"""
OpenAI Agent Tools for Frontend Generation
Specialized tools for generating and fixing dApp frontends
"""

import os
import json
import subprocess
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# Base React project template
PACKAGE_JSON_TEMPLATE = {
    "name": "aleo-dapp",
    "version": "0.1.0",
    "private": True,
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.14.2",
        "typescript": "^4.9.5",
        "@types/react": "^18.2.15",
        "@types/react-dom": "^18.2.7",
        "@types/node": "^16.18.39",
        "web3": "^4.1.1"
    },
    "devDependencies": {
        "@vitejs/plugin-react": "^4.0.3",
        "autoprefixer": "^10.4.14",
        "postcss": "^8.4.27",
        "tailwindcss": "^3.3.3",
        "vite": "^4.4.5"
    },
    "scripts": {
        "dev": "vite",
        "build": "tsc && vite build",
        "preview": "vite preview"
    }
}

TSCONFIG_TEMPLATE = {
    "compilerOptions": {
        "target": "ES2020",
        "useDefineForClassFields": True,
        "lib": ["ES2020", "DOM", "DOM.Iterable"],
        "module": "ESNext",
        "skipLibCheck": True,
        "moduleResolution": "bundler",
        "allowImportingTsExtensions": True,
        "resolveJsonModule": True,
        "isolatedModules": True,
        "noEmit": True,
        "jsx": "react-jsx",
        "strict": True,
        "noUnusedLocals": True,
        "noUnusedParameters": True,
        "noFallthroughCasesInSwitch": True
    },
    "include": ["src"],
    "references": [{"path": "./tsconfig.node.json"}]
}

VITE_CONFIG_TEMPLATE = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})"""

TAILWIND_CONFIG_TEMPLATE = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'aleo-blue': '#0055FF',
        'aleo-cyan': '#00D4FF',
        'aleo-pink': '#FF0099',
        'aleo-dark': '#0A0E27',
      }
    },
  },
  plugins: [],
}"""

POSTCSS_CONFIG_TEMPLATE = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""

INDEX_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Aleo dApp</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""

MAIN_TSX_TEMPLATE = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""

INDEX_CSS_TEMPLATE = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}"""


def create_project_structure(project_path: str) -> Dict[str, Any]:
    """Create the basic project structure for a React + TypeScript + Tailwind project"""
    try:
        # Create directories
        dirs = ['src', 'src/components', 'src/pages', 'src/utils', 'public']
        for dir_path in dirs:
            os.makedirs(os.path.join(project_path, dir_path), exist_ok=True)
        
        # Create configuration files
        files_to_create = {
            'package.json': json.dumps(PACKAGE_JSON_TEMPLATE, indent=2),
            'tsconfig.json': json.dumps(TSCONFIG_TEMPLATE, indent=2),
            'tsconfig.node.json': json.dumps({
                "compilerOptions": {
                    "composite": True,
                    "skipLibCheck": True,
                    "module": "ESNext",
                    "moduleResolution": "bundler",
                    "allowSyntheticDefaultImports": True
                },
                "include": ["vite.config.ts"]
            }, indent=2),
            'vite.config.ts': VITE_CONFIG_TEMPLATE,
            'tailwind.config.js': TAILWIND_CONFIG_TEMPLATE,
            'postcss.config.js': POSTCSS_CONFIG_TEMPLATE,
            'index.html': INDEX_HTML_TEMPLATE,
            '.gitignore': 'node_modules\n.DS_Store\ndist\ndist-ssr\n*.local\n.vscode/*\n!.vscode/extensions.json\n.idea\n*.suo\n*.ntvs*\n*.njsproj\n*.sln\n*.sw?',
            'src/main.tsx': MAIN_TSX_TEMPLATE,
            'src/index.css': INDEX_CSS_TEMPLATE,
            'src/vite-env.d.ts': '/// <reference types="vite/client" />'
        }
        
        for file_path, content in files_to_create.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'success': True,
            'message': 'Project structure created successfully',
            'files_created': list(files_to_create.keys())
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def install_dependencies(project_path: str) -> Dict[str, Any]:
    """Install npm dependencies for the project"""
    try:
        logger.info("Installing dependencies...")
        result = subprocess.run(
            ['npm', 'install'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'message': 'Dependencies installed successfully'
            }
        else:
            return {
                'success': False,
                'error': result.stderr,
                'stdout': result.stdout
            }
            
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'npm install timed out after 5 minutes'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def parse_build_errors(error_output: str) -> List[Dict[str, Any]]:
    """Parse build errors from TypeScript/Vite output"""
    errors = []
    
    # TypeScript error pattern
    ts_error_pattern = r'(.+\.tsx?):(\d+):(\d+) - error TS\d+: (.+)'
    for match in re.finditer(ts_error_pattern, error_output):
        errors.append({
            'type': 'typescript',
            'file': match.group(1),
            'line': int(match.group(2)),
            'column': int(match.group(3)),
            'message': match.group(4)
        })
    
    # Import error pattern
    import_error_pattern = r"Cannot find module '(.+)'"
    for match in re.finditer(import_error_pattern, error_output):
        errors.append({
            'type': 'import',
            'module': match.group(1),
            'message': f"Cannot find module '{match.group(1)}'"
        })
    
    # JSX error pattern
    jsx_error_pattern = r"(.+\.tsx?):(\d+):(\d+): (.+)"
    for match in re.finditer(jsx_error_pattern, error_output):
        if not any(e['file'] == match.group(1) and e['line'] == int(match.group(2)) for e in errors):
            errors.append({
                'type': 'jsx',
                'file': match.group(1),
                'line': int(match.group(2)),
                'column': int(match.group(3)),
                'message': match.group(4)
            })
    
    return errors


def generate_app_component(contract_name: str, transitions: List[Dict[str, Any]]) -> str:
    """Generate the main App component based on contract analysis"""
    
    # Group transitions by category
    categories = {}
    for transition in transitions:
        category = _categorize_transition(transition['name'])
        if category not in categories:
            categories[category] = []
        categories[category].append(transition)
    
    # Generate route imports
    route_imports = []
    routes = []
    
    for category, trans_list in categories.items():
        component_name = category.replace('_', ' ').title().replace(' ', '') + 'Page'
        route_imports.append(f"import {component_name} from './pages/{component_name}'")
        routes.append(f'          <Route path="/{category.replace("_", "-")}" element={{<{component_name} />}} />')
    
    imports_str = '\n'.join(route_imports)
    routes_str = '\n'.join(routes)
    
    return f"""import React from 'react'
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
{imports_str}

function App() {{
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header contractName="{contract_name}" />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={{<HomePage />}} />
{routes_str}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}}

export default App"""


def generate_header_component(contract_name: str) -> str:
    """Generate Header component"""
    return f"""import React from 'react'
import {{ Link }} from 'react-router-dom'

interface HeaderProps {{
  contractName: string
}}

const Header: React.FC<HeaderProps> = ({{ contractName }}) => {{
  return (
    <header className="bg-aleo-dark text-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold">
            {{contractName}} dApp
          </Link>
          <nav>
            <ul className="flex space-x-6">
              <li><Link to="/" className="hover:text-aleo-cyan transition">Home</Link></li>
              <li><Link to="/operations" className="hover:text-aleo-cyan transition">Operations</Link></li>
              <li><Link to="/about" className="hover:text-aleo-cyan transition">About</Link></li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  )
}}

export default Header"""


def generate_footer_component() -> str:
    """Generate Footer component with AleoForge branding"""
    return """import React from 'react'

const Footer: React.FC = () => {
  return (
    <footer className="bg-aleo-dark text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="text-center">
          <p className="text-lg">
            Made with <span className="text-red-500">❤️</span> by{' '}
            <span className="font-bold text-aleo-cyan">AleoForge</span>
          </p>
          <p className="text-sm text-gray-400 mt-2">
            Building the future of decentralized applications on Aleo
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer"""


def generate_home_page() -> str:
    """Generate Home page component"""
    return """import React from 'react'
import { Link } from 'react-router-dom'

const HomePage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold text-center mb-8 text-aleo-dark">
          Welcome to Your Aleo dApp
        </h1>
        
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-4">About This dApp</h2>
          <p className="text-gray-600 mb-6">
            This decentralized application is built on the Aleo blockchain, 
            providing privacy-preserving smart contract functionality.
          </p>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-aleo-blue to-aleo-cyan p-6 rounded-lg text-white">
              <h3 className="text-xl font-semibold mb-2">Private by Default</h3>
              <p>All transactions are private unless explicitly made public</p>
            </div>
            
            <div className="bg-gradient-to-br from-aleo-pink to-pink-500 p-6 rounded-lg text-white">
              <h3 className="text-xl font-semibold mb-2">Zero-Knowledge Proofs</h3>
              <p>Powered by cutting-edge cryptography for maximum privacy</p>
            </div>
          </div>
        </div>
        
        <div className="text-center">
          <Link 
            to="/operations" 
            className="inline-block bg-aleo-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-600 transition"
          >
            Get Started
          </Link>
        </div>
      </div>
    </div>
  )
}

export default HomePage"""


def _categorize_transition(name: str) -> str:
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