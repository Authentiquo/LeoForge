#!/usr/bin/env python3
"""
LeoForge - AI-powered Leo code generator for Aleo blockchain
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Run the main module
from src.main import main

if __name__ == "__main__":
    main() 