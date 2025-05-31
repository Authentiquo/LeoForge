# Frontend Pipeline for Aleo Smart Contracts

This pipeline generates modern dApp frontends from Aleo smart contracts using AI agents.

## Features

- **Smart Contract Analysis**: Automatically analyzes Aleo contracts to understand their structure
- **Progressive Generation**: Generates frontend components page by page
- **Error Detection & Fixing**: Automatically detects and fixes compilation errors
- **Modern Tech Stack**: React + TypeScript + Tailwind CSS + Vite
- **AleoForge Branding**: All generated dApps include "Made with ❤️ by AleoForge" footer

## Usage

### Using the Agent Pipeline (Recommended)

```python
from frontend_pipeline import generate_dapp_frontend

# Generate a dApp frontend from an Aleo contract
result = generate_dapp_frontend(
    contract_path="path/to/contract.aleo",
    output_dir="generated_frontends"
)

if result['success']:
    print(f"Frontend generated at: {result['project_path']}")
```

### Using the Progressive Pipeline

```python
from frontend_pipeline import generate_progressive_frontend

# Generate with progressive error fixing
result = generate_progressive_frontend(
    contract_path="path/to/contract.aleo",
    output_dir="generated_frontends"
)
```

## Architecture

The pipeline consists of several specialized agents:

1. **Smart Contract Analyzer**: Analyzes the Aleo contract structure
2. **Frontend Architect**: Designs the frontend architecture
3. **React Developer**: Generates React components
4. **Error Detective**: Detects build errors
5. **Code Fixer**: Fixes detected errors

## Generated Structure

```
generated_frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   └── [Contract-specific pages]
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── index.html
```

## Requirements

- Node.js 16+
- npm or yarn
- Python 3.8+
- OpenAI Agents SDK (optional)

## Development

To extend the pipeline:

1. Add new tools in `openai_agent_tools.py`
2. Create new agents in `agent_pipeline.py`
3. Implement custom error fixes in `refactored_pipeline.py` 