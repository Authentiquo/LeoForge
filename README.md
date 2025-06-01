<div align="center">

# ⚡ LeoForge

</div>

<div align="center">

![LeoForge Logo](https://img.shields.io/badge/🔥_LeoForge-v1.0.0-ff6b35?style=for-the-badge&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Leo](https://img.shields.io/badge/Leo-Compatible-00d4aa?style=for-the-badge&logo=aleo&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-9d4edd?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-Powered Leo Smart Contract Generator for Aleo Blockchain**

*Transform your ideas into production-ready Leo smart contracts with the power of artificial intelligence*

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Documentation](#documentation) • [Roadmap](#roadmap)

</div>

---

## Overview

**LeoForge** is a revolutionary AI-powered code generation framework specifically designed for creating Leo smart contracts on the Aleo blockchain. It leverages cutting-edge language models and a sophisticated multi-agent architecture to transform natural language descriptions into compilable, secure, and optimized Leo smart contracts.

### Key Highlights

- **Multi-Agent AI System**: Specialized AI agents working in perfect harmony
- **Iterative Refinement**: Automatic compilation, error detection, and intelligent correction
- **Security-First**: Built-in security analysis and best practices enforcement
- **Dual Interface**: Rich CLI and beautiful Web UI (Streamlit)
- **Learning System**: Analyzes errors and improves future generations
- **Production Ready**: Generates deployable, tested smart contracts

## ✨ Features

### Multi-Agent Architecture
- **Architect Agent**: Analyzes requirements and designs optimal project architecture
- **Code Generator Agent**: Generates high-quality Leo code with best practices
- **Code Evaluator Agent**: Reviews code for completeness, security, and optimization
- **Rule Engineer Agent**: Learns from errors and creates improvement rules

### Intelligent Workflow
- **Iterative Improvement**: Automatic compilation and error correction loop
- **Smart Error Analysis**: AI-powered error diagnosis and fixing
- **Quality Assurance**: Comprehensive code evaluation with scoring
- **Build Integration**: Direct Leo CLI integration for testing

### Rich User Experience
- **Beautiful CLI**: Rich console interface with progress tracking
- **Web Interface**: Modern Streamlit-based web application
- **Real-time Feedback**: Live progress updates and detailed results
- **Project Management**: Automatic workspace creation and organization

### Security & Quality
- **Security Analysis**: Built-in vulnerability detection
- **Best Practices**: Enforced Leo coding standards
- **Code Review**: AI-powered code quality assessment
- **Testing Integration**: Automatic test generation and execution

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Leo CLI** - [Install Leo](https://developer.aleo.org/leo/installation)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **AI API Key** - Get from [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/LeoForge.git
   cd LeoForge
   ```

2. **Install Python virtual environment support** (if needed)
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install python3-venv
   
   # CentOS/RHEL/Fedora
   sudo yum install python3-venv  # or dnf install python3-venv
   
   # macOS (usually included with Python)
   # Windows (included with Python installation)
   ```

3. **Create and activate virtual environment**
   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (Command Prompt)
   python -m venv venv
   venv\Scripts\activate
   
   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   ANTHROPIC_API_KEY=your-anthropic-api-key-here
   # OR
   OPENAI_API_KEY=your-openai-api-key-here
   
   # Optional: Custom admin address for generated contracts
   ADMIN_ADDRESS=aleo1your_admin_address_here
   ```

6. **Verify Leo CLI installation**
   ```bash
   leo --version
   ```

### Alternative: Quick Setup Script

Or use the automatic setup script for easier installation:

```bash
# Make the script executable
chmod +x launch.sh

# Launch LeoForge (automatically configures environment)
./launch.sh generate

# For web interface
./launch.sh
```

The `launch.sh` script automatically handles:
- Creating virtual environment if it doesn't exist
- Activating it
- Installing dependencies if needed
- Checking Leo CLI presence
- Launching the application

### Usage Options

#### Command Line Interface (CLI)

**Interactive Mode** (Recommended for beginners):
```bash
python main.py generate
```

**Direct Command Mode**:
```bash
# Generate a token with specific type
python main.py generate "Create a governance token with voting and delegation" --type token

# Custom iterations and non-interactive mode
python main.py generate "Build a DeFi lending protocol" --iterations 3 --no-interactive
```

**View Examples**:
```bash
python main.py examples
```

**Manage Configuration**:
```bash
# View current configuration
python main.py config

# Update admin address
python main.py config --set-admin aleo1your_new_admin_address
```

**Rule Management** (Learning System):
```bash
# Analyze logs and generate improvement rules
python main.py analyze-logs

# View generated rules
python main.py rules

# Export rules
python main.py rules --export my_rules.json
```

#### Web Interface (Streamlit)

Launch the beautiful web interface:
```bash
streamlit run app.py
```

Or use the convenient launcher script:
```bash
./launch.sh
```

Then open your browser to `http://localhost:8501`

## 🏗️ Architecture

### Workflow Diagram

```mermaid
graph TB
    %% Styles pour les sous-graphes avec des couleurs plus vives
    classDef ui fill:#e1f5fe,stroke:#0288d1,stroke-width:3px,color:#01579b,font-size:14px,font-weight:bold;
    classDef core fill:#fff8e1,stroke:#ff8f00,stroke-width:3px,color:#e65100,font-size:14px,font-weight:bold;
    classDef agent fill:#e8f5e9,stroke:#4caf50,stroke-width:3px,color:#1b5e20,font-size:14px,font-weight:bold;
    classDef services fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px,color:#4a148c,font-size:14px,font-weight:bold;
    classDef storage fill:#ffebee,stroke:#f44336,stroke-width:3px,color:#b71c1c,font-size:14px,font-weight:bold;
    
    %% Styles pour les nœuds avec des couleurs de fond gradient
    classDef uiNode fill:linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%),stroke:#1976d2,stroke-width:2px,color:#fff,font-weight:bold;
    classDef coreNode fill:linear-gradient(135deg, #ffb74d 0%, #ffa726 100%),stroke:#f57c00,stroke-width:2px,color:#fff,font-weight:bold;
    classDef agentNode fill:linear-gradient(135deg, #81c784 0%, #66bb6a 100%),stroke:#388e3c,stroke-width:2px,color:#fff,font-weight:bold;
    classDef serviceNode fill:linear-gradient(135deg, #ba68c8 0%, #ab47bc 100%),stroke:#7b1fa2,stroke-width:2px,color:#fff,font-weight:bold;
    classDef storageNode fill:linear-gradient(135deg, #ef5350 0%, #e53935 100%),stroke:#c62828,stroke-width:2px,color:#fff,font-weight:bold;

    subgraph UI["🖥️ Interface Utilisateur"]
        A["💻 Web UI<br/>Streamlit Dashboard"]
        B["⌨️ CLI<br/>Rich Console Interface"]
    end
    class UI ui;
    class A,B uiNode;

    subgraph CORE["🎯 Orchestration Centrale"]
        C["🎼 Project Orchestrator<br/>Gestionnaire de Workflow"]
    end
    class CORE core;
    class C coreNode;

    subgraph AGENTS["🤖 Couche d'Agents IA"]
        D["🏗️ Architect Agent<br/>Conception Architecture"]
        E["⚡ Code Generator<br/>Génération Leo Code"]
        F["🔍 Code Evaluator<br/>Évaluation Qualité"]
        G["📚 Rule Engineer<br/>Apprentissage & Règles"]
    end
    class AGENTS agent;
    class D,E,F,G agentNode;

    subgraph SERVICES["⚙️ Couche de Services"]
        H["🔨 Leo Builder<br/>Service de Compilation"]
        I["📁 Workspace Manager<br/>Gestion de Projets"]
        J["📊 Logger Service<br/>Suivi des Erreurs"]
        K["🧠 Rule Manager<br/>Base de Connaissances"]
    end
    class SERVICES services;
    class H,I,J,K serviceNode;

    subgraph STORAGE["💾 Stockage & Sortie"]
        L["📄 Generated Code<br/>Smart Contracts Leo"]
        M["📈 Project Logs<br/>Analyse des Erreurs"]
        N["📖 Improvement Rules<br/>Base d'Apprentissage"]
        O["🚀 Compiled Output<br/>Contrats Déployables"]
    end
    class STORAGE storage;
    class L,M,N,O storageNode;

    %% Flux de l'interface utilisateur avec des flèches colorées
    A ==>|"Interface Web"| C
    B ==>|"Ligne de commande"| C

    %% Workflow principal des agents
    C ==>|"Initialisation"| D
    D ==>|"Architecture définie"| E
    E ==>|"Code généré"| F
    F ==>|"Évaluation"| G

    %% Intégration des services
    C -.->|"Build Request"| H
    C -.->|"Project Setup"| I
    C -.->|"Log Events"| J
    G -.->|"Update Rules"| K

    %% Boucles de rétroaction avec des styles différents
    F -->|"❌ Amélioration requise"| E
    H -->|"🔥 Erreurs de build"| E
    G -->|"✨ Nouvelles règles"| D
    G -->|"🎯 Optimisations"| E

    %% Génération des sorties
    E ==>|"💾 Sauvegarde"| L
    J ==>|"📝 Journalisation"| M
    G ==>|"🧠 Apprentissage"| N
    H ==>|"🎯 Compilation"| O

    %% Flux de données supplémentaires
    K -.->|"📚 Règles appliquées"| D
    K -.->|"🎯 Patterns"| E
    I -.->|"📁 Structure projet"| E
    M -.->|"📈 Analytics"| G
```

### Agent Responsibilities

| Agent | Role | Key Functions |
|-------|------|---------------|
| **Architect** | System Designer | • Analyzes natural language requirements<br/>• Designs optimal data structures<br/>• Plans contract architecture<br/>• Considers security implications |
| **Code Generator** | Code Creator | • Transforms requirements into Leo code<br/>• Implements all specified features<br/>• Follows Leo syntax and best practices<br/>• Handles compilation error fixes |
| **Code Evaluator** | Quality Assessor | • Evaluates code completeness<br/>• Identifies security vulnerabilities<br/>• Suggests optimizations<br/>• Provides quality scores (1-10) |
| **Rule Engineer** | Learning System | • Analyzes error patterns<br/>• Creates improvement rules<br/>• Builds knowledge base<br/>• Enhances future generations |

### Iterative Improvement Process

1. **Requirement Analysis**: Architect Agent processes user input
2. **Architecture Design**: Creates optimal contract structure
3. **Code Generation**: Generates initial Leo smart contract
4. **Quality Evaluation**: Assesses code quality and completeness
5. **Compilation Test**: Attempts to build with Leo CLI
6. **Iterative Refinement**: Fixes errors and improves code
7. **Final Validation**: Produces deployable contract

### Advanced Features

#### Rule Learning System

LeoForge includes an intelligent learning system that analyzes errors and creates improvement rules:

```bash
# Analyze error logs and generate rules
python main.py analyze-logs

# View generated rules
python main.py rules

# Export rules for sharing
python main.py rules --export team_rules.json
```

#### Configuration Management

```bash
# View current configuration
python main.py config

# Update admin address for contracts
python main.py config --set-admin aleo1your_admin_address

# View admin-specific settings
python main.py config --admin
```

#### Project Analytics

Every generation run is logged and analyzed:

- **Error Tracking**: Comprehensive error logging and analysis
- **Performance Metrics**: Build times, iteration counts, success rates
- **Quality Scores**: AI-powered code quality assessment
- **Improvement Suggestions**: Actionable recommendations

## 📋 Roadmap

### Current Version (v1.0.0)
- ✅ Multi-agent AI architecture
- ✅ CLI and web interfaces
- ✅ Leo compilation integration
- ✅ Rule learning system
- ✅ Error analysis and correction
- ✅ Project type support (Token, NFT, DeFi, Game, Oracle)

### Next Release (v1.1.0) - Q2 2024
- **Enhanced AI Models**: Support for latest Claude and GPT models
- **Testing Framework**: Automatic test generation for generated contracts
- **Template System**: Pre-built templates for common contract patterns
- **Security Auditing**: Advanced security analysis with vulnerability scoring
- **Documentation Generation**: Automatic README and API documentation
- **Multi-language Support**: Support for additional programming languages

### Future Releases (v2.0.0+) - 2024
- **Multi-contract Projects**: Support for complex, interconnected contract systems
- **Collaboration Features**: Team workspaces and shared rule databases
- **UI/UX Improvements**: Enhanced web interface with visual contract designer
- **Analytics Dashboard**: Comprehensive project analytics and insights
- **CI/CD Integration**: GitHub Actions and automated deployment workflows
- **Cloud Deployment**: Hosted version with API access
- **Plugin System**: Extensible architecture for custom agents and tools
- **Mobile App**: Mobile interface for contract generation and management

### Long-term Vision
- **Advanced AI Integration**: Custom-trained models for Leo-specific code generation
- **Enterprise Features**: Advanced team management and enterprise security
- **Ecosystem Integration**: Deep integration with Aleo ecosystem tools
- **Market Intelligence**: Smart contract analytics and market insights
- **Predictive Analysis**: AI-powered performance and security predictions

## Contributing

We welcome contributions from the community! Here's how you can help:

### Bug Reports
Found a bug? Please open an issue with:
- Detailed description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

### Feature Requests
Have an idea? We'd love to hear it! Please include:
- Clear description of the feature
- Use cases and benefits
- Implementation suggestions (if any)

### Development

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Ensure tests pass**: `pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for public methods
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Aleo Team** - For creating the innovative Leo programming language
- **Anthropic & OpenAI** - For providing powerful AI models
- **Rich Library** - For the beautiful console interface
- **Streamlit** - For the amazing web framework
- **Open Source Community** - For inspiration and contributions

---

<div align="center">

**Made with ❤️ for the Aleo Ecosystem**

*Transform your blockchain ideas into reality with LeoForge*

[⭐ Star us on GitHub](https://github.com/yourusername/LeoForge) • [📖 Documentation](https://docs.leoforge.dev) • [💬 Discord](https://discord.gg/leoforge)

</div>