"""
Rule Manager - Manages storage and retrieval of Leo rules for prompt enrichment
"""
import json
from pathlib import Path
from typing import List, Dict
from src.models import LeoRule, RuleType


class RuleManager:
    """Manages Leo rules for prompt enrichment"""
    
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = Path(rules_dir)
        self.rules_dir.mkdir(exist_ok=True)
        self.rules_file = self.rules_dir / "leo_rules.json"
        self.rules_cache = self._load_rules()
    
    def _load_rules(self) -> Dict[str, List[LeoRule]]:
        """Load rules from file"""
        if self.rules_file.exists():
            with open(self.rules_file, 'r') as f:
                data = json.load(f)
                
            rules = {
                "architect": [],
                "codex": []
            }
            
            for rule_type, rule_list in data.items():
                for rule_data in rule_list:
                    rule = LeoRule(**rule_data)
                    rules[rule_type].append(rule)
            
            return rules
        
        return {"architect": [], "codex": []}
    
    def save_rules(self, architect_rules: List[LeoRule], codex_rules: List[LeoRule]):
        """Save rules to file"""
        # Merge with existing rules
        for rule in architect_rules:
            if not any(r.rule_id == rule.rule_id for r in self.rules_cache["architect"]):
                self.rules_cache["architect"].append(rule)
        
        for rule in codex_rules:
            if not any(r.rule_id == rule.rule_id for r in self.rules_cache["codex"]):
                self.rules_cache["codex"].append(rule)
        
        # Convert to dict for JSON
        data = {
            "architect": [rule.dict() for rule in self.rules_cache["architect"]],
            "codex": [rule.dict() for rule in self.rules_cache["codex"]]
        }
        
        with open(self.rules_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_architect_rules(self, limit: int = 10) -> List[LeoRule]:
        """Get top architect rules by priority"""
        rules = sorted(
            self.rules_cache["architect"], 
            key=lambda r: r.priority, 
            reverse=True
        )
        return rules[:limit]
    
    def get_codex_rules(self, limit: int = 10) -> List[LeoRule]:
        """Get top codex rules by priority"""
        rules = sorted(
            self.rules_cache["codex"], 
            key=lambda r: r.priority, 
            reverse=True
        )
        return rules[:limit]
    
    def format_rules_for_prompt(self, rules: List[LeoRule]) -> str:
        """Format rules for inclusion in agent prompts"""
        if not rules:
            return ""
        
        formatted = "\n\nLEARNED RULES FROM PREVIOUS RUNS:\n"
        formatted += "=" * 50 + "\n\n"
        
        for i, rule in enumerate(rules, 1):
            formatted += f"{i}. {rule.title}\n"
            formatted += f"   Description: {rule.description}\n"
            formatted += f"   Pattern to avoid: {rule.pattern}\n"
            formatted += f"   Solution: {rule.solution}\n"
            
            if rule.examples:
                formatted += f"   Examples:\n"
                for example in rule.examples[:2]:  # Limit examples
                    formatted += f"      - {example}\n"
            
            formatted += f"   Priority: {rule.priority}/10\n\n"
        
        formatted += "=" * 50 + "\n"
        formatted += "Apply these rules to avoid common mistakes and improve code quality.\n"
        
        return formatted 