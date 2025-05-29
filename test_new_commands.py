#!/usr/bin/env python3
"""
Test script for the new manual rule generation commands
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and return the result"""
    print(f"\n🔧 Running: {cmd}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Test the new CLI commands"""
    print("🧪 Testing LeoForge Manual Rule Generation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("src/cli.py").exists():
        print("❌ Please run this script from the LeoForge root directory")
        sys.exit(1)
    
    # Test commands
    commands = [
        # Test help for new commands
        "python -m src.cli analyze-logs --help",
        "python -m src.cli rules --help",
        
        # Test listing logs
        "python -m src.cli analyze-logs --list",
        
        # Test listing rules
        "python -m src.cli rules",
        
        # Test rules with type filter
        "python -m src.cli rules --type architect",
        "python -m src.cli rules --type codex",
    ]
    
    success_count = 0
    total_count = len(commands)
    
    for cmd in commands:
        if run_command(cmd):
            success_count += 1
            print("✅ Command succeeded")
        else:
            print("❌ Command failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_count} commands succeeded")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    print("\n📋 Manual Testing Steps:")
    print("1. Generate a project with errors: leoforge generate 'complex defi protocol'")
    print("2. List available logs: leoforge analyze-logs --list")
    print("3. Analyze a log: leoforge analyze-logs")
    print("4. View generated rules: leoforge rules")
    print("5. Export rules: leoforge rules --export test_rules.json")

if __name__ == "__main__":
    main() 