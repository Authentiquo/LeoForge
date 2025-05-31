#!/usr/bin/env python3
"""
Script to generate frontend for navigo_discount_verifier contract
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

from frontend_pipeline.pipeline import FrontendArchitect

def main():
    print("🚀 Generating frontend for navigo_discount_verifier...")
    print("=" * 60)
    
    # Initialize the architect
    architect = FrontendArchitect('generated_frontends')
    
    # Path to the contract
    contract_path = 'output/navigo_discount_verifier/src/main.leo'
    
    if not os.path.exists(contract_path):
        print(f"❌ Contract not found at: {contract_path}")
        return
    
    print(f"📄 Processing contract: {contract_path}")
    
    # Build frontend
    try:
        result = architect.build_frontend_project(
            contract_path, 
            'navigo_discount_verifier_frontend'
        )
        
        if result['success']:
            print("\n✨ Frontend generated successfully!")
            print(f"📁 Location: {os.path.abspath(result['frontend_path'])}")
            
            print(f"\n📋 Project Specifications:")
            specs = result['specifications']
            print(f"   - Project: {specs['project_name']}")
            print(f"   - Pages: {len(specs['pages'])}")
            print(f"   - Features: {len(specs['features'])}")
            
            print(f"\n📄 Generated Pages:")
            for page in specs['pages']:
                print(f"   - {page['name']} ({page['route']})")
            
            print(f"\n🎨 Design System:")
            design = specs['design_system']
            print(f"   - Primary Color: {design['colors']['primary']}")
            print(f"   - Typography: {design['typography']['headings']}")
            print(f"   - Components: Glass morphism with animations")
            
            if 'qa_report' in result:
                print(f"\n✅ Quality Assurance:")
                qa = result['qa_report']
                print(f"   - Status: {qa.get('overall_status', 'Completed')}")
                if 'passed' in qa:
                    print(f"   - Checks Passed: {len(qa['passed'])}")
                if 'failed' in qa:
                    print(f"   - Checks Failed: {len(qa['failed'])}")
            
            print(f"\n🚀 Next Steps:")
            print(f"   1. cd {result['frontend_path']}")
            print(f"   2. npm install")
            print(f"   3. npm start")
            print(f"   4. Open http://localhost:3000")
            
        else:
            print(f"\n❌ Error: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 