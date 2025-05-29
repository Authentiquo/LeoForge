#!/usr/bin/env python3
"""
Test script for the Frontend Architect Pipeline
Tests the new architect approach to building beautiful frontend projects
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend_pipeline.pipeline import FrontendArchitect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_architect_pipeline():
    """Test the Frontend Architect pipeline with a sample contract"""
    
    print("🚀 Testing Frontend Architect Pipeline")
    print("=" * 50)
    
    # Path to test contract
    test_contract = os.path.join(
        os.path.dirname(__file__), 
        '..', '..', 'examples', 'amine_token.aleo'
    )
    
    if not os.path.exists(test_contract):
        print(f"❌ Test contract not found at: {test_contract}")
        print("Creating a sample contract for testing...")
        
        # Create examples directory if it doesn't exist
        examples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'examples')
        os.makedirs(examples_dir, exist_ok=True)
        
        # Create a sample Aleo contract
        sample_contract = '''program amine_token.aleo {
    // Token record
    record Token {
        owner: address,
        amount: u64,
    }
    
    // Mappings
    mapping account: address => u64;
    mapping frozen_accounts: address => bool;
    mapping total_supply: bool => u64;
    
    // Constants
    const MAX_SUPPLY: u64 = 1000000000u64;
    const DECIMALS: u8 = 6u8;
    
    // Initialize the token
    transition initialize(initial_supply: u64) -> Token {
        assert(initial_supply <= MAX_SUPPLY);
        return Token {
            owner: self.caller,
            amount: initial_supply,
        };
    }
    
    // Mint new tokens
    transition mint_public(receiver: address, amount: u64) {
        return then finalize(receiver, amount);
    }
    
    finalize mint_public(receiver: address, amount: u64) {
        let current_supply: u64 = Mapping::get_or_use(total_supply, true, 0u64);
        let new_supply: u64 = current_supply + amount;
        assert(new_supply <= MAX_SUPPLY);
        
        Mapping::set(total_supply, true, new_supply);
        let current_balance: u64 = Mapping::get_or_use(account, receiver, 0u64);
        Mapping::set(account, receiver, current_balance + amount);
    }
    
    // Transfer tokens
    transition transfer_public(receiver: address, amount: u64) {
        return then finalize(self.caller, receiver, amount);
    }
    
    finalize transfer_public(sender: address, receiver: address, amount: u64) {
        let sender_balance: u64 = Mapping::get_or_use(account, sender, 0u64);
        assert(sender_balance >= amount);
        
        Mapping::set(account, sender, sender_balance - amount);
        let receiver_balance: u64 = Mapping::get_or_use(account, receiver, 0u64);
        Mapping::set(account, receiver, receiver_balance + amount);
    }
    
    // Burn tokens
    transition burn_public(amount: u64) {
        return then finalize(self.caller, amount);
    }
    
    finalize burn_public(burner: address, amount: u64) {
        let balance: u64 = Mapping::get_or_use(account, burner, 0u64);
        assert(balance >= amount);
        
        Mapping::set(account, burner, balance - amount);
        let current_supply: u64 = Mapping::get_or_use(total_supply, true, 0u64);
        Mapping::set(total_supply, true, current_supply - amount);
    }
    
    // Freeze account (admin only)
    transition freeze_account(target: address) {
        return then finalize(target);
    }
    
    finalize freeze_account(target: address) {
        Mapping::set(frozen_accounts, target, true);
    }
    
    // Check balance
    transition check_balance(account_address: address) -> u64 {
        return 0u64;
    }
}'''
        
        test_contract = os.path.join(examples_dir, 'amine_token.aleo')
        with open(test_contract, 'w') as f:
            f.write(sample_contract)
        print(f"✅ Created sample contract at: {test_contract}")
    
    # Initialize the architect
    output_dir = "architect_generated_frontends"
    architect = FrontendArchitect(output_dir)
    
    print(f"\n📁 Output directory: {output_dir}")
    print(f"📄 Processing contract: {test_contract}")
    print("\n" + "=" * 50 + "\n")
    
    # Process the contract
    try:
        result = architect.build_frontend_project(test_contract, "modern_token_app")
        
        if result['success']:
            print("\n✨ Frontend project generated successfully!")
            print(f"\n📋 Project Specifications:")
            print(f"   - Pages: {len(result['specifications']['pages'])}")
            print(f"   - Features: {len(result['specifications']['features'])}")
            print(f"   - Design System: Modern with glassmorphism")
            
            print(f"\n📄 Generated Pages:")
            for page in result['specifications']['pages']:
                print(f"   - {page['name']} ({page['route']})")
            
            print(f"\n✅ Quality Assurance:")
            print(f"   - Status: {result['qa_report']['overall_status']}")
            print(f"   - Checks Passed: {len(result['qa_report']['passed'])}")
            print(f"   - Checks Failed: {len(result['qa_report']['failed'])}")
            
            print(f"\n🧪 Startup Test:")
            print(f"   - Status: {result['test_result']['status']}")
            
            print(f"\n🚀 Next Steps:")
            print(f"   1. cd {result['frontend_path']}")
            print(f"   2. npm install")
            print(f"   3. npm start")
            print(f"   4. Open http://localhost:3000")
            
            print(f"\n📁 Frontend location: {os.path.abspath(result['frontend_path'])}")
            
            # Display architect report
            report_path = os.path.join(result['frontend_path'], 'architect_report.json')
            if os.path.exists(report_path):
                print(f"\n📊 Architect Report saved at: {report_path}")
            
        else:
            print(f"\n❌ Error: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        logger.exception("Error in architect pipeline test")


def test_batch_processing():
    """Test batch processing of multiple contracts"""
    
    print("\n\n🚀 Testing Batch Processing")
    print("=" * 50)
    
    # Create additional test contracts
    examples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'examples')
    os.makedirs(examples_dir, exist_ok=True)
    
    # Banking contract
    banking_contract = '''program banking_system.aleo {
    record Account {
        owner: address,
        balance: u64,
    }
    
    mapping accounts: address => u64;
    mapping loan_amounts: address => u64;
    
    transition create_account(initial_deposit: u64) -> Account {
        return Account {
            owner: self.caller,
            balance: initial_deposit,
        };
    }
    
    transition deposit(amount: u64) {
        return then finalize(self.caller, amount);
    }
    
    finalize deposit(depositor: address, amount: u64) {
        let current: u64 = Mapping::get_or_use(accounts, depositor, 0u64);
        Mapping::set(accounts, depositor, current + amount);
    }
    
    transition withdraw(amount: u64) {
        return then finalize(self.caller, amount);
    }
    
    finalize withdraw(withdrawer: address, amount: u64) {
        let balance: u64 = Mapping::get_or_use(accounts, withdrawer, 0u64);
        assert(balance >= amount);
        Mapping::set(accounts, withdrawer, balance - amount);
    }
}'''
    
    with open(os.path.join(examples_dir, 'banking_system.aleo'), 'w') as f:
        f.write(banking_contract)
    
    # Process multiple contracts
    architect = FrontendArchitect("architect_batch_frontends")
    
    contracts = ['amine_token.aleo', 'banking_system.aleo']
    
    for contract_name in contracts:
        contract_path = os.path.join(examples_dir, contract_name)
        if os.path.exists(contract_path):
            print(f"\n📄 Processing: {contract_name}")
            result = architect.build_frontend_project(contract_path)
            
            if result['success']:
                print(f"   ✅ Success! Generated at: {result['frontend_path']}")
            else:
                print(f"   ❌ Failed: {result['error']}")


if __name__ == "__main__":
    # Test single contract processing
    test_architect_pipeline()
    
    # Test batch processing
    # test_batch_processing()
    
    print("\n\n✨ All tests completed!")
    print("=" * 50) 