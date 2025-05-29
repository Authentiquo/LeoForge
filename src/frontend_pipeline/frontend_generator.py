"""
Frontend Generator for React Applications
Generates React components and pages based on smart contract analysis
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass
from .contract_analyzer import ContractInfo, Transition


@dataclass
class PageInfo:
    """Information about a page to generate"""
    name: str
    path: str
    components: List[str]
    transitions: List[str]


class FrontendGenerator:
    """Generates React frontend code based on contract analysis"""
    
    def __init__(self, output_dir: str = "generated_frontend"):
        self.output_dir = output_dir
        self.contract_info = None
        self.pages = []
    
    def generate(self, contract_info: ContractInfo, project_name: str = None) -> str:
        """Generate complete React frontend based on contract info"""
        self.contract_info = contract_info
        self.project_name = project_name or contract_info.program_name
        
        # Create output directory
        frontend_dir = os.path.join(self.output_dir, self.project_name)
        os.makedirs(frontend_dir, exist_ok=True)
        
        # Generate React app structure
        self._generate_package_json(frontend_dir)
        self._generate_app_structure(frontend_dir)
        self._generate_pages(frontend_dir)
        self._generate_components(frontend_dir)
        self._generate_styles(frontend_dir)
        
        return frontend_dir
    
    def _generate_package_json(self, base_dir: str):
        """Generate package.json file"""
        package_json = f'''{{
  "name": "{self.project_name}-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.2",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4",
    "axios": "^1.4.0",
    "tailwindcss": "^3.3.3",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "@heroicons/react": "^2.0.18"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "eslintConfig": {{
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  }},
  "browserslist": {{
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }}
}}'''
        
        with open(os.path.join(base_dir, 'package.json'), 'w') as f:
            f.write(package_json)
    
    def _generate_app_structure(self, base_dir: str):
        """Generate basic app structure"""
        # Create directories
        dirs = ['src', 'src/components', 'src/pages', 'src/styles', 'src/utils', 'public']
        for dir_path in dirs:
            os.makedirs(os.path.join(base_dir, dir_path), exist_ok=True)
        
        # Generate index.html
        index_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{self.project_name} - Aleo Smart Contract Frontend" />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>{self.project_name.replace('_', ' ').title()}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
        
        with open(os.path.join(base_dir, 'public', 'index.html'), 'w') as f:
            f.write(index_html)
        
        # Generate tailwind config
        tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'aleo-blue': '#0055FF',
        'aleo-dark': '#001133',
        'aleo-light': '#E6F0FF',
      }
    },
  },
  plugins: [],
}'''
        
        with open(os.path.join(base_dir, 'tailwind.config.js'), 'w') as f:
            f.write(tailwind_config)
        
        # Generate index.js
        index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();'''
        
        with open(os.path.join(base_dir, 'src', 'index.js'), 'w') as f:
            f.write(index_js)
        
        # Generate reportWebVitals.js
        report_web_vitals = '''const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;'''
        
        with open(os.path.join(base_dir, 'src', 'reportWebVitals.js'), 'w') as f:
            f.write(report_web_vitals)
        
        # Generate App.js
        self._generate_app_js(base_dir)
    
    def _generate_app_js(self, base_dir: str):
        """Generate main App.js file"""
        # Determine pages based on transitions
        pages = self._determine_pages()
        
        # Generate routes
        routes = []
        imports = []
        for page in pages:
            imports.append(f"import {page['component']} from './pages/{page['component']}';")
            routes.append(f"          <Route path=\"{page['path']}\" element={{<{page['component']} />}} />")
        
        app_js = f'''import React from 'react';
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
{chr(10).join(imports)}
import './styles/App.css';

function App() {{
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={{<Home />}} />
{chr(10).join(routes)}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}}

export default App;'''
        
        with open(os.path.join(base_dir, 'src', 'App.js'), 'w') as f:
            f.write(app_js)
    
    def _determine_pages(self) -> List[Dict[str, str]]:
        """Determine pages to generate based on contract transitions"""
        pages = []
        
        # Group transitions by functionality
        transition_groups = {
            'token': ['mint', 'transfer', 'burn'],
            'account': ['create_account', 'deposit', 'withdraw'],
            'admin': ['freeze', 'pause', 'admin', 'initialize'],
            'nft': ['nft', 'claim', 'metadata'],
            'public': ['public_to_private', 'private_to_public']
        }
        
        # Check which groups are needed
        transition_names = [t.name.lower() for t in self.contract_info.transitions]
        
        for group, keywords in transition_groups.items():
            if any(keyword in name for name in transition_names for keyword in keywords):
                component_name = f"{group.title()}Operations"
                pages.append({
                    'component': component_name,
                    'path': f'/{group}',
                    'title': f'{group.title()} Operations'
                })
        
        # Add a dashboard page if there are mappings
        if self.contract_info.mappings:
            pages.append({
                'component': 'Dashboard',
                'path': '/dashboard',
                'title': 'Dashboard'
            })
        
        return pages
    
    def _generate_pages(self, base_dir: str):
        """Generate page components"""
        pages_dir = os.path.join(base_dir, 'src', 'pages')
        
        # Generate Home page
        self._generate_home_page(pages_dir)
        
        # Generate other pages
        pages = self._determine_pages()
        for page in pages:
            self._generate_page(pages_dir, page)
    
    def _generate_home_page(self, pages_dir: str):
        """Generate home page"""
        transitions_list = '\n'.join([
            f"              <li className=\"flex items-center space-x-2\">"
            f"<span className=\"text-aleo-blue\">•</span>"
            f"<span>{t.name.replace('_', ' ').title()}</span>"
            f"</li>"
            for t in self.contract_info.transitions[:5]
        ])
        
        home_page = f'''import React from 'react';
import {{ Link }} from 'react-router-dom';
import {{ CubeTransparentIcon, CircleStackIcon, CodeBracketIcon }} from '@heroicons/react/24/outline';

const Home = () => {{
  return (
    <div className="space-y-12">
      {{/* Hero Section */}}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          {self.project_name.replace('_', ' ').title()}
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          A powerful Aleo smart contract interface for decentralized operations
        </p>
      </section>

      {{/* Features Grid */}}
      <section className="grid md:grid-cols-3 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <CubeTransparentIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Smart Contract</h3>
          <p className="text-gray-600">
            Built on Aleo blockchain with privacy-preserving technology
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <CircleStackIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Data Storage</h3>
          <p className="text-gray-600">
            {len(self.contract_info.mappings)} mappings and {len(self.contract_info.records)} record types
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <CodeBracketIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Functions</h3>
          <p className="text-gray-600">
            {len(self.contract_info.transitions)} transitions available
          </p>
        </div>
      </section>

      {{/* Contract Info */}}
      <section className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold mb-6">Contract Overview</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-3">Available Operations</h3>
            <ul className="space-y-2 text-gray-600">
{transitions_list}
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-3">Contract Stats</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Transitions:</span>
                <span className="font-semibold">{len(self.contract_info.transitions)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Mappings:</span>
                <span className="font-semibold">{len(self.contract_info.mappings)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Records:</span>
                <span className="font-semibold">{len(self.contract_info.records)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Constants:</span>
                <span className="font-semibold">{len(self.contract_info.constants)}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {{/* Call to Action */}}
      <section className="text-center py-8">
        <Link
          to="/dashboard"
          className="inline-block bg-aleo-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Get Started
        </Link>
      </section>
    </div>
  );
}};

export default Home;'''
        
        with open(os.path.join(pages_dir, 'Home.js'), 'w') as f:
            f.write(home_page)
    
    def _generate_page(self, pages_dir: str, page_info: Dict[str, str]):
        """Generate a specific page"""
        # Find relevant transitions for this page
        relevant_transitions = []
        page_keywords = page_info['path'].strip('/').split('_')
        
        for transition in self.contract_info.transitions:
            if any(keyword in transition.name.lower() for keyword in page_keywords):
                relevant_transitions.append(transition)
        
        # Generate forms for transitions
        forms = []
        for i, transition in enumerate(relevant_transitions[:3]):  # Limit to 3 forms per page
            forms.append(self._generate_transition_form(transition))
        
        page_content = f'''import React, {{ useState }} from 'react';
import {{ ArrowPathIcon }} from '@heroicons/react/24/outline';

const {page_info['component']} = () => {{
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e, transitionName) => {{
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {{
      setResult({{
        success: true,
        message: `${{transitionName}} executed successfully!`,
        txId: `0x${{Math.random().toString(16).substr(2, 8)}}`
      }});
      setLoading(false);
    }}, 1500);
  }};

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{page_info['title']}</h1>
        <p className="mt-2 text-gray-600">
          Manage {page_info['path'].strip('/').replace('_', ' ')} operations on the Aleo blockchain
        </p>
      </div>

      {{/* Result Display */}}
      {{result && (
        <div className={{`p-4 rounded-lg ${{result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}}`}}>
          <p className={{`font-semibold ${{result.success ? 'text-green-800' : 'text-red-800'}}`}}>
            {{result.message}}
          </p>
          {{result.txId && (
            <p className="text-sm text-gray-600 mt-1">
              Transaction ID: {{result.txId}}
            </p>
          )}}
        </div>
      )}}

      {{/* Forms */}}
      <div className="space-y-6">
        {chr(10).join(forms) if forms else self._generate_placeholder_form(page_info['title'])}
      </div>
    </div>
  );
}};

export default {page_info['component']};'''
        
        with open(os.path.join(pages_dir, f"{page_info['component']}.js"), 'w') as f:
            f.write(page_content)
    
    def _generate_transition_form(self, transition: Transition) -> str:
        """Generate a form for a transition"""
        form_fields = []
        for param in transition.parameters:
            if param['visibility'] == 'public':
                field_type = 'text'
                if param['type'] in ['u64', 'u32', 'u8', 'u128']:
                    field_type = 'number'
                elif param['type'] == 'bool':
                    field_type = 'checkbox'
                
                form_fields.append(f'''          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {param['name'].replace('_', ' ').title()}
            </label>
            <input
              type="{field_type}"
              name="{param['name']}"
              {'checked' if field_type == 'checkbox' else 'required'}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter {param['name'].replace('_', ' ')}"
            />
          </div>''')
        
        return f'''        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            {transition.name.replace('_', ' ').title()}
          </h2>
          <form onSubmit={{(e) => handleSubmit(e, '{transition.name}')}} className="space-y-4">
{chr(10).join(form_fields) if form_fields else '            <p className="text-gray-600">This function requires private parameters</p>'}
            <button
              type="submit"
              disabled={{loading}}
              className="w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {{loading ? (
                <span className="flex items-center justify-center">
                  <ArrowPathIcon className="animate-spin h-5 w-5 mr-2" />
                  Processing...
                </span>
              ) : (
                'Execute'
              )}}
            </button>
          </form>
        </div>'''
    
    def _generate_placeholder_form(self, title: str) -> str:
        """Generate a placeholder form when no specific transitions are found"""
        return f'''        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">{title}</h2>
          <p className="text-gray-600 mb-4">
            This section provides access to {title.lower()} functionality.
          </p>
          <button
            onClick={{() => alert('Feature coming soon!')}}
            className="w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
          >
            Coming Soon
          </button>
        </div>'''
    
    def _generate_components(self, base_dir: str):
        """Generate reusable components"""
        components_dir = os.path.join(base_dir, 'src', 'components')
        
        # Generate Navbar
        self._generate_navbar(components_dir)
        
        # Generate Footer
        self._generate_footer(components_dir)
        
        # Generate Dashboard if needed
        if any(page['component'] == 'Dashboard' for page in self._determine_pages()):
            self._generate_dashboard(os.path.join(base_dir, 'src', 'pages'))
    
    def _generate_navbar(self, components_dir: str):
        """Generate Navbar component"""
        pages = self._determine_pages()
        nav_links = []
        for page in pages[:4]:  # Limit to 4 main nav items
            nav_links.append(f'''            <Link
              to="{page['path']}"
              className="text-gray-700 hover:text-aleo-blue transition-colors"
            >
              {page['title']}
            </Link>''')
        
        navbar = f'''import React from 'react';
import {{ Link }} from 'react-router-dom';

const Navbar = () => {{
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-aleo-blue rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              {self.project_name.replace('_', ' ').title()}
            </span>
          </Link>
          
          <div className="flex space-x-6">
{chr(10).join(nav_links)}
          </div>
        </div>
      </div>
    </nav>
  );
}};

export default Navbar;'''
        
        with open(os.path.join(components_dir, 'Navbar.js'), 'w') as f:
            f.write(navbar)
    
    def _generate_footer(self, components_dir: str):
        """Generate Footer component"""
        footer = '''import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">
              © 2024 All rights reserved
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm">Powered by Aleo</span>
            <span className="text-sm text-gray-400">•</span>
            <span className="text-sm font-semibold">Made with AleoForge</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;'''
        
        with open(os.path.join(components_dir, 'Footer.js'), 'w') as f:
            f.write(footer)
    
    def _generate_dashboard(self, pages_dir: str):
        """Generate Dashboard page"""
        # Create mapping cards
        mapping_cards = []
        for mapping in self.contract_info.mappings[:4]:
            mapping_cards.append(f'''        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-2">{mapping.name.replace('_', ' ').title()}</h3>
          <p className="text-sm text-gray-600 mb-4">
            {mapping.key_type} → {mapping.value_type}
          </p>
          <div className="text-2xl font-bold text-aleo-blue">
            {{Math.floor(Math.random() * 1000)}}
          </div>
          <p className="text-sm text-gray-500 mt-1">Total entries</p>
        </div>''')
        
        dashboard = f'''import React from 'react';
import {{ ChartBarIcon, UsersIcon, CurrencyDollarIcon, ClockIcon }} from '@heroicons/react/24/outline';

const Dashboard = () => {{
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Monitor and analyze your smart contract activity
        </p>
      </div>

      {{/* Stats Grid */}}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
{chr(10).join(mapping_cards) if mapping_cards else '''        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-2">Total Transactions</h3>
          <div className="text-2xl font-bold text-aleo-blue">
            {Math.floor(Math.random() * 10000)}
          </div>
        </div>'''}
      </div>

      {{/* Activity Chart Placeholder */}}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Activity Overview</h2>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
          <div className="text-center">
            <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-500">Activity chart visualization</p>
          </div>
        </div>
      </div>

      {{/* Recent Transactions */}}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Transaction ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {{[...Array(5)].map((_, i) => (
                <tr key={{i}}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    0x{{Math.random().toString(16).substr(2, 8)}}...
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{['Transfer', 'Mint', 'Deposit', 'Withdraw'][Math.floor(Math.random() * 4)]}}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Success
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{i + 1}} minutes ago
                  </td>
                </tr>
              ))}}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}};

export default Dashboard;'''
        
        with open(os.path.join(pages_dir, 'Dashboard.js'), 'w') as f:
            f.write(dashboard)
    
    def _generate_styles(self, base_dir: str):
        """Generate CSS files"""
        styles_dir = os.path.join(base_dir, 'src', 'styles')
        
        # Generate index.css with Tailwind imports
        index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}'''
        
        with open(os.path.join(styles_dir, 'index.css'), 'w') as f:
            f.write(index_css)
        
        # Generate App.css
        app_css = '''/* Custom styles for the app */
.App {
  text-align: center;
}

/* Loading spinner */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}'''
        
        with open(os.path.join(styles_dir, 'App.css'), 'w') as f:
            f.write(app_css) 