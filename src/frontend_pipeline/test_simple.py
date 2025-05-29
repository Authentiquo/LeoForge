"""
Simple test script for Frontend Pipeline
Tests the basic functionality without OpenAI Agents
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.frontend_pipeline.contract_analyzer import ContractAnalyzer
from src.frontend_pipeline.frontend_generator import FrontendGenerator


def test_analyzer():
    """Test the contract analyzer"""
    print("=" * 60)
    print("Testing Contract Analyzer")
    print("=" * 60)
    
    # Read a sample contract
    contract_path = "output/amine_token/src/main.leo"
    
    if os.path.exists(contract_path):
        with open(contract_path, 'r') as f:
            contract_content = f.read()
        
        # Analyze contract
        analyzer = ContractAnalyzer()
        contract_info = analyzer.analyze(contract_content)
        summary = analyzer.get_contract_summary()
        
        print(f"\n✅ Contract analyzed successfully!")
        print(f"Program: {contract_info.program_name}")
        print(f"\n📊 Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        return contract_info
    else:
        print(f"❌ Contract file not found: {contract_path}")
        return None


def test_generator(contract_info):
    """Test the frontend generator"""
    print("\n" + "=" * 60)
    print("Testing Frontend Generator")
    print("=" * 60)
    
    if not contract_info:
        print("❌ No contract info available")
        return
    
    # Generate frontend
    generator = FrontendGenerator(output_dir="generated_frontends_test")
    frontend_path = generator.generate(contract_info)
    
    print(f"\n✅ Frontend generated successfully!")
    print(f"📁 Output directory: {frontend_path}")
    
    # Check generated files
    print("\n📂 Generated structure:")
    for root, dirs, files in os.walk(frontend_path):
        level = root.replace(frontend_path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Limit to first 5 files per directory
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files) - 5} more files")
    
    # Verify footer has AleoForge
    footer_path = os.path.join(frontend_path, 'src', 'components', 'Footer.js')
    if os.path.exists(footer_path):
        with open(footer_path, 'r') as f:
            content = f.read()
            if 'Made with AleoForge' in content:
                print("\n✅ Footer contains 'Made with AleoForge'")
            else:
                print("\n❌ Footer missing 'Made with AleoForge'")
    
    return frontend_path


def test_multiple_contracts():
    """Test with multiple contracts"""
    print("\n" + "=" * 60)
    print("Testing Multiple Contracts")
    print("=" * 60)
    
    contracts = [
        ("output/amine_token/src/main.leo", "amine_token"),
        ("output/banking_system/src/main.leo", "banking_system"),
        ("nft_randomized_system_corrected.aleo", "nft_system")
    ]
    
    generator = FrontendGenerator(output_dir="generated_frontends_test")
    
    for contract_path, name in contracts:
        if os.path.exists(contract_path):
            print(f"\n📝 Processing: {name}")
            
            with open(contract_path, 'r') as f:
                content = f.read()
            
            analyzer = ContractAnalyzer()
            info = analyzer.analyze(content)
            
            if info.program_name:
                frontend_path = generator.generate(info, name)
                print(f"   ✅ Generated at: {frontend_path}")
            else:
                print(f"   ❌ Failed to analyze contract")
        else:
            print(f"\n⚠️  Skipping {name} (file not found)")


def main():
    """Main test function"""
    print("\n🚀 Simple Frontend Pipeline Test\n")
    
    # Test analyzer
    contract_info = test_analyzer()
    
    # Test generator
    if contract_info:
        test_generator(contract_info)
    
    # Test multiple contracts
    test_multiple_contracts()
    
    print("\n✨ All tests completed!")
    print("\n📖 To run a generated frontend:")
    print("   cd generated_frontends_test/[project_name]")
    print("   npm install")
    print("   npm start")


if __name__ == "__main__":
    main() 