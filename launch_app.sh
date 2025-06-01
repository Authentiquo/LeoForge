#!/bin/bash

# LeoForge Streamlit App Launcher

echo "🚀 Starting LeoForge Web Interface..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Set PYTHONPATH to include current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Launch Streamlit app
echo "Launching Streamlit app on http://localhost:8501"
echo ""
streamlit run app.py --server.port 8501 --server.address localhost 