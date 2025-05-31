#!/usr/bin/env python3
"""Test frontend generation for navigo_discount_verifier"""

from src.frontend_pipeline import generate_progressive_frontend

# Générer le frontend pour navigo_discount_verifier
result = generate_progressive_frontend(
    contract_path='output/navigo_discount_verifier/build/main.aleo',
    output_dir='generated_frontends'
)

if result['success']:
    print(f'✅ Frontend généré avec succès !')
    print(f'📁 Chemin : {result["project_path"]}')
    print(f'📋 Contrat : {result["contract_name"]}')
    print(f'🔧 Transitions : {result["transitions"]}')
    print(f'\nPour lancer le frontend :')
    print(f'cd {result["project_path"]}')
    print(f'npm install')
    print(f'npm run dev')
else:
    print(f'❌ Erreur : {result["error"]}') 