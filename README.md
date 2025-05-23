# LeoForge

LeoForge is an AI-powered workflow that generates Leo code for the Aleo blockchain using OpenAI's Agents SDK.

## Features

- Built with OpenAI's Agents SDK for advanced agentic capabilities
- Specialized multi-agent architecture with handoffs between expert agents
- Built-in function tools for Leo project operations
- AI-assisted generation of Leo smart contracts
- Interactive workflow with human-in-the-loop validation
- LLM evaluation of generated code
- Support for multi-component contract composition
- Easy project building and deployment
- Comprehensive Leo cheatsheet with async programming examples
- Modern async/await programming model implementation

## Architecture

LeoForge uses a multi-agent architecture powered by the OpenAI Agents SDK:

1. **Architect Agent**: Analyzes requirements and designs component structures
2. **Generator Agent**: Creates Leo code based on specifications
3. **Evaluator Agent**: Checks code quality and provides feedback
4. **Builder Agent**: Handles project creation and compilation

Agents work together through handoffs, allowing them to delegate tasks to each other based on their specializations.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key and other configuration in .env
```

## Usage

```bash
python leoforge.py
```

Follow the interactive prompts to generate Leo code based on your specifications.

### Advanced Configuration

Enable tracing for debugging by setting:

```
ENABLE_TRACING=true
```

in your .env file to visualize agent interactions and workflow.

## Leo Programming Resources

The repository includes comprehensive resources for Leo programming:

- **System Prompt**: A detailed prompt that guides the AI in generating proper Leo code
- **Leo Cheatsheet**: A complete reference for Leo syntax, including:
  - Basic data types and structures
  - Transitions and functions
  - Async programming model with Futures
  - Mapping operations for on-chain storage
  - Best practices and common pitfalls

These resources are continuously updated to reflect the latest changes in the Leo language and Aleo blockchain. 