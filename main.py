#!/usr/bin/env python3
"""
LeoForge - AI-Powered Leo Smart Contract Generator
Main entry point for the application
"""
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.cli import main

if __name__ == "__main__":
    main() 