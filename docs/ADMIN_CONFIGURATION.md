# Configuration Admin - LeoForge 🔐

## Vue d'ensemble

LeoForge intègre maintenant une gestion centralisée des adresses administrateurs pour les contrats Leo. Cette fonctionnalité permet aux architectes et générateurs de code de créer des contrats avec des fonctionnalités administratives appropriées.

## Configuration par défaut

L'adresse admin par défaut est configurée dans le fichier `.env` :

```bash
# Admin address for Leo blockchain operations
ADMIN_ADDRESS=aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc
```

## Fichiers modifiés

### 1. `.env.example`
- ✅ Ajout de `ADMIN_ADDRESS` avec l'adresse par défaut
- ✅ Documentation claire du paramètre admin

### 2. `src/config.py` (nouveau)
- ✅ Classe `LeoForgeConfig` pour la gestion centralisée des configurations
- ✅ Validation des adresses Aleo
- ✅ Chargement automatique des variables d'environnement
- ✅ Méthodes utilitaires pour la gestion admin

### 3. `src/models.py`
- ✅ Ajout de `admin_features` et `requires_admin` à `ArchitectureDesign`
- ✅ Support des fonctionnalités admin dans l'architecture

### 4. `src/leoagents/architect.py`
- ✅ Intégration de la configuration admin
- ✅ Utilisation des modèles par défaut depuis la configuration
- ✅ Instructions renforcées pour les fonctionnalités admin

### 5. `src/leoagents/code_generator.py`
- ✅ Génération de code avec support admin
- ✅ Patterns de contrôle d'accès intégrés
- ✅ Utilisation de l'adresse admin dans les templates

### 6. `src/leoagents/code_evaluator.py`
- ✅ Évaluation des fonctionnalités admin
- ✅ Vérification des contrôles d'accès admin

### 7. `src/leoagents/prompt.py`
- ✅ Templates mis à jour pour inclure les informations admin
- ✅ Instructions d'évaluation pour les fonctionnalités admin

### 8. `src/cli.py`
- ✅ Nouvelle commande `config` pour afficher/modifier la configuration
- ✅ Support de l'affichage et modification de l'adresse admin

## Utilisation

### Afficher la configuration actuelle

```bash
# Afficher toute la configuration
python main.py config

# Afficher spécifiquement la configuration admin
python main.py config --admin
```

### Modifier l'adresse admin

```bash
# Changer l'adresse admin
python main.py config --set-admin aleo1your_new_admin_address_here
```

### Test de la configuration

Un script de test est disponible pour vérifier la configuration :

```bash
python test_admin_config.py
```

## Fonctionnalités admin dans les contrats

Quand l'Architect détermine qu'un projet nécessite des fonctionnalités admin, il peut :

1. **Marquer le projet comme nécessitant un admin** : `requires_admin: true`
2. **Lister les fonctionnalités admin** : dans `admin_features`
3. **Le générateur implémente les contrôles d'accès** avec l'adresse admin configurée

### Exemple de pattern de contrôle d'accès Leo

```leo
// Fonction admin uniquement
async transition admin_mint(amount: u64) -> Future {
    // Vérification que l'appelant est l'admin
    assert_eq(self.caller, aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc);
    
    // Logique de mint admin
    return self.complete_admin_mint(amount);
}
```

## Validation des adresses

Le système valide automatiquement les adresses Aleo :
- ✅ Commence par `aleo1`
- ✅ Longueur de 63 caractères
- ✅ Caractères alphanumériques uniquement

## Architecture modulaire

La configuration admin est maintenant intégrée dans tout le pipeline :

```
UserQuery -> Architect (avec config admin) -> CodeGenerator (avec patterns admin) -> CodeEvaluator (validation admin)
```

## Prochaines étapes

L'architecte peut maintenant utiliser cette fonctionnalité pour :
- Créer des contrats avec des rôles admin appropriés
- Implémenter des contrôles d'accès robustes
- Suivre les meilleures pratiques de sécurité Leo/Aleo

---

**Note** : Cette fonctionnalité est entièrement intégrée et prête à être utilisée. L'architecte décidera au cas par cas si les fonctionnalités admin sont nécessaires pour chaque projet généré. 