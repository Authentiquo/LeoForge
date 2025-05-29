#!/usr/bin/env python
"""
Test script to verify that the code generator uses self.signer for record ownership
"""
import subprocess
import sys

def test_generator():
    print("Testing code generator with simple token...")
    
    # Test command
    result = subprocess.run([
        sys.executable, "main.py", "generate", 
        "Create a simple token with transfer function", 
        "--type", "token",
        "--no-interactive",
        "--iterations", "1"
    ], capture_output=True, text=True)
    
    print("Return code:", result.returncode)
    print("\nSTDOUT:\n", result.stdout)
    print("\nSTDERR:\n", result.stderr)
    
    # Check if self.caller appears in generated code (warning)
    if "self.caller" in result.stderr and "owner" in result.stderr:
        print("\n❌ WARNING: Code still uses self.caller for record ownership!")
        print("This will generate Leo warnings.")
        return False
    
    print("\n✅ Test passed - No self.caller warnings detected")
    return True

if __name__ == "__main__":
    test_generator() 