#!/usr/bin/env python3
"""
Test script for the Simplified Frontend Architect
Tests the simplified version without AI agents
"""

import os
import sys
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend_pipeline.pipeline_simple import SimpleFrontendArchitect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def test_simple_architect():
    """Test the simplified frontend architect"""
    
    print("🚀 Testing Simplified Frontend Architect")
    print("=" * 50)
    
    # Create test contract if needed
    test_contract = os.path.join(
        os.path.dirname(__file__), 
        '..', '..', 'examples', 'amine_token.aleo'
    )
    
    if not os.path.exists(test_contract):
        print("Creating test contract...")
        examples_dir = os.path.dirname(test_contract)
        os.makedirs(examples_dir, exist_ok=True)
        
        with open(test_contract, 'w') as f:
            f.write('''program amine_token.aleo {
    record Token {
        owner: address,
        amount: u64,
    }
    
    mapping account: address => u64;
    mapping frozen_accounts: address => bool;
    mapping total_supply: bool => u64;
    
    const MAX_SUPPLY: u64 = 1000000000u64;
    
    transition initialize(initial_supply: u64) -> Token {
        return Token {
            owner: self.caller,
            amount: initial_supply,
        };
    }
    
    transition mint_public(receiver: address, amount: u64) {
        return then finalize(receiver, amount);
    }
    
    transition transfer_public(receiver: address, amount: u64) {
        return then finalize(self.caller, receiver, amount);
    }
    
    transition burn_public(amount: u64) {
        return then finalize(self.caller, amount);
    }
}''')
    
    # Initialize architect
    architect = SimpleFrontendArchitect("simple_generated_frontends")
    
    # Process contract
    print(f"\n📄 Processing: {test_contract}")
    result = architect.build_frontend_project(test_contract, "beautiful_token_app")
    
    if result['success']:
        print("\n✨ Success! Frontend generated!")
        print(f"\n📋 Specifications:")
        print(f"   - Pages: {len(result['specifications']['pages'])}")
        print(f"   - Features: {len(result['specifications']['features'])}")
        
        print(f"\n📄 Pages generated:")
        for page in result['specifications']['pages']:
            print(f"   - {page['name']} ({page['route']})")
        
        print(f"\n📁 Location: {result['frontend_path']}")
        print(f"\n🚀 Next steps:")
        for step in result['report']['next_steps']:
            print(f"   {step}")
    else:
        print(f"\n❌ Error: {result['error']}")


if __name__ == "__main__":
    test_simple_architect()
    print("\n✨ Test completed!") 