#!/bin/bash
# LeoForge launcher script

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import rich" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found.${NC}"
    echo -e "${YELLOW}Please set your API key:${NC}"
    echo -e "${YELLOW}  export ANTHROPIC_API_KEY=your-key${NC}"
    echo -e "${YELLOW}  or${NC}"
    echo -e "${YELLOW}  export OPENAI_API_KEY=your-key${NC}"
fi

# Check if Leo is installed
if ! command -v leo &> /dev/null; then
    echo -e "${RED}❌ Leo CLI not found. Please install Leo first.${NC}"
    echo -e "${YELLOW}   Visit: https://developer.aleo.org/leo/installation${NC}"
    exit 1
fi

# Run LeoForge
echo -e "${GREEN}🚀 Starting LeoForge...${NC}"
echo ""
python3 main.py "$@" 