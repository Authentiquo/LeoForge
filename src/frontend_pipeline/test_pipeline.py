"""
Test script for the Frontend Pipeline
Demonstrates generating React frontends from Aleo smart contracts
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.frontend_pipeline import FrontendPipeline


def test_single_contract():
    """Test generating frontend for a single contract"""
    print("=" * 60)
    print("Frontend Pipeline Test - Single Contract")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = FrontendPipeline(output_dir="generated_frontends")
    
    # Test with amine_token contract
    contract_path = "output/amine_token/src/main.leo"
    
    if os.path.exists(contract_path):
        print(f"\nProcessing contract: {contract_path}")
        result = pipeline.process_contract(contract_path)
        
        if result['success']:
            print("\n✅ Frontend generated successfully!")
            print(f"📁 Output directory: {result['frontend_path']}")
            print(f"\n📊 Statistics:")
            stats = result['report']['statistics']
            for key, value in stats.items():
                print(f"   - {key}: {value}")
            
            print(f"\n📄 Generated pages:")
            for page in result['report']['pages']:
                print(f"   - {page['name']} ({page['path']})")
            
            print(f"\n🚀 To run the frontend:")
            instructions = result['report']['instructions']
            print(f"   1. {instructions['install']}")
            print(f"   2. {instructions['run']}")
        else:
            print(f"\n❌ Error: {result['error']}")
    else:
        print(f"\n❌ Contract file not found: {contract_path}")


def test_multiple_contracts():
    """Test generating frontends for multiple contracts"""
    print("\n" + "=" * 60)
    print("Frontend Pipeline Test - Multiple Contracts")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = FrontendPipeline(output_dir="generated_frontends")
    
    # List of contracts to process
    contracts = [
        "output/amine_token/src/main.leo",
        "output/banking_system/src/main.leo",
        "nft_randomized_system_corrected.aleo"
    ]
    
    for contract_path in contracts:
        if os.path.exists(contract_path):
            print(f"\n📝 Processing: {os.path.basename(contract_path)}")
            result = pipeline.process_contract(contract_path)
            
            if result['success']:
                print(f"   ✅ Success! Frontend at: {result['frontend_path']}")
            else:
                print(f"   ❌ Failed: {result['error']}")
        else:
            print(f"\n⚠️  Skipping (not found): {contract_path}")


def test_contract_analyzer():
    """Test the contract analyzer component"""
    print("\n" + "=" * 60)
    print("Contract Analyzer Test")
    print("=" * 60)
    
    from src.frontend_pipeline.contract_analyzer import ContractAnalyzer
    
    analyzer = ContractAnalyzer()
    
    # Test with a simple contract snippet
    test_contract = """
program test_token.aleo {
    record Token {
        owner: address,
        amount: u64,
    }
    
    mapping balances: address => u64;
    
    const ADMIN: address = aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0;
    
    transition mint(receiver: address, amount: u64) -> Token {
        return Token {
            owner: receiver,
            amount: amount,
        };
    }
    
    async transition transfer(public receiver: address, public amount: u64) -> Future {
        return finalize_transfer(self.signer, receiver, amount);
    }
}
    """
    
    info = analyzer.analyze(test_contract)
    summary = analyzer.get_contract_summary()
    
    print(f"\n📊 Analysis Results:")
    print(f"   Program: {info.program_name}")
    print(f"   Records: {[r.name for r in info.records]}")
    print(f"   Mappings: {[m.name for m in info.mappings]}")
    print(f"   Transitions: {[t.name for t in info.transitions]}")
    print(f"   Constants: {[c.name for c in info.constants]}")


def main():
    """Main test function"""
    print("\n🚀 AleoForge Frontend Pipeline Test Suite\n")
    
    # Run tests
    test_contract_analyzer()
    test_single_contract()
    test_multiple_contracts()
    
    print("\n✨ All tests completed!")


if __name__ == "__main__":
    main() 