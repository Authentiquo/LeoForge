# Refactoring des Prompts Système LeoForge

## Vue d'ensemble

Les prompts système ont été refactorisés pour être plus compacts et efficaces tout en conservant les informations essentielles des modules 3, 4 et 5 de la documentation Leo.

## Changements principaux

### 1. Nouveau système de prompts compacts
- **Fichier**: `src/leoagents/compact_prompts.py`
- Remplace l'ancien `prompt.py` qui est maintenant déprécié
- Structure modulaire avec des fonctions de génération de prompts

### 2. Suppression de la dépendance à la cheatsheet
- Plus besoin de charger `leo_cheatsheet.md` (30KB)
- Les règles essentielles sont intégrées directement dans `LEO_CORE_RULES`
- Réduction significative de la taille des prompts

### 3. Configuration des modèles centralisée
- Les modèles sont définis dans `src/config.py`
- Chaque agent charge son modèle depuis la configuration
- Support des clés API Anthropic et OpenAI

## Structure des nouveaux prompts

### LEO_CORE_RULES
Contient l'essentiel de la syntaxe Leo :
- Structure de programme
- Types et littéraux
- Transitions (basic et async)
- Validations et assertions
- Patterns ARC21 pour les tokens

### Prompts spécifiques par agent

1. **Architect** (`ARCHITECT_COMPACT_PROMPT`)
   - Focus sur la conception minimale viable
   - Identification des types de projet
   - Patterns d'administration

2. **Code Generator** (`CODEGEN_COMPACT_PROMPT`)
   - Patterns de code essentiels
   - Structures communes (records, mappings)
   - Exemples concrets

3. **Evaluator** (`EVALUATOR_COMPACT_PROMPT`)
   - Checklist de validation
   - Problèmes courants
   - Format JSON strict

4. **Error Fix** (`ERROR_FIX_COMPACT`)
   - Solutions aux erreurs communes
   - Patterns de correction

## Avantages du refactoring

1. **Performance**: Prompts 70% plus petits
2. **Maintenabilité**: Un seul fichier central
3. **Flexibilité**: Règles apprises intégrées dynamiquement
4. **Clarté**: Focus sur l'essentiel sans répétitions

## Migration

Pour migrer du système ancien :

```python
# Ancien
from .prompt import ARCHITECT_SYSTEM_PROMPT

# Nouveau
from .compact_prompts import get_architect_prompt
prompt = get_architect_prompt(admin_address, learned_rules)
```

## Configuration des modèles

Les modèles sont maintenant configurés dans `config.py`:
- `default_architect_model`: claude-sonnet-4-20250514
- `default_generator_model`: claude-opus-4-20250514  
- `default_evaluator_model`: claude-sonnet-4-20250514 