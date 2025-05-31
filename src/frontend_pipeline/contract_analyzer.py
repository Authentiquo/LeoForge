"""
Contract Analyzer for Aleo Smart Contracts
Parses and extracts components from .aleo smart contract files
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class ContractComponent:
    """Base class for contract components"""
    name: str
    raw_content: str = ""


@dataclass
class Record(ContractComponent):
    """Represents a record in the contract"""
    fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class Mapping(ContractComponent):
    """Represents a mapping in the contract"""
    key_type: str = ""
    value_type: str = ""


@dataclass
class Transition(ContractComponent):
    """Represents a transition (function) in the contract"""
    parameters: List[Dict[str, str]] = field(default_factory=list)
    returns: List[str] = field(default_factory=list)
    is_async: bool = False
    visibility: str = "public"


@dataclass
class Constant(ContractComponent):
    """Represents a constant in the contract"""
    type_: str = ""
    value: str = ""


@dataclass
class ContractInfo:
    """Contains all parsed information from a contract"""
    program_name: str
    records: List[Record] = field(default_factory=list)
    mappings: List[Mapping] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)
    constants: List[Constant] = field(default_factory=list)
    structs: List[Dict[str, Any]] = field(default_factory=list)


class ContractAnalyzer:
    """Analyzes Aleo smart contracts and extracts components"""
    
    def __init__(self):
        self.contract_info = None
    
    def analyze(self, contract_content: str) -> ContractInfo:
        """Analyze contract content and extract all components"""
        self.contract_info = ContractInfo(program_name="")
        
        # Detect if it's a compiled .aleo file or source .leo file
        is_compiled = "program " in contract_content and "function " in contract_content
        
        if is_compiled:
            self._analyze_compiled_aleo(contract_content)
        else:
            self._analyze_source_leo(contract_content)
        
        return self.contract_info
    
    def _analyze_compiled_aleo(self, content: str):
        """Analyze compiled .aleo file format"""
        # Extract program name from compiled format: program name.aleo;
        program_match = re.search(r'program\s+(\w+)\.aleo;', content)
        if program_match:
            self.contract_info.program_name = program_match.group(1)
        
        # Extract records from compiled format
        record_pattern = r'record\s+(\w+):\s*\n((?:\s+\w+\s+as\s+[\w\.]+\s*;\s*\n)+)'
        for match in re.finditer(record_pattern, content):
            record_name = match.group(1)
            record_body = match.group(2)
            
            record = Record(name=record_name)
            
            # Extract fields: owner as address.private;
            field_pattern = r'(\w+)\s+as\s+([\w\.]+)\s*;'
            for field_match in re.finditer(field_pattern, record_body):
                field_name = field_match.group(1)
                field_type = field_match.group(2).replace('.private', '').replace('.public', '')
                record.fields[field_name] = field_type
            
            self.contract_info.records.append(record)
        
        # Extract mappings from compiled format
        mapping_pattern = r'mapping\s+(\w+):\s*\n\s*key\s+as\s+([\w\.]+)\s*;\s*\n\s*value\s+as\s+([\w\.]+)\s*;'
        for match in re.finditer(mapping_pattern, content):
            mapping = Mapping(
                name=match.group(1),
                key_type=match.group(2).replace('.public', '').replace('.private', ''),
                value_type=match.group(3).replace('.public', '').replace('.private', '')
            )
            self.contract_info.mappings.append(mapping)
        
        # Extract functions (transitions) from compiled format
        function_pattern = r'function\s+(\w+):((?:\s*input\s+\w+\s+as\s+[\w\.]+\s*;\s*\n)*)'
        for match in re.finditer(function_pattern, content):
            function_name = match.group(1)
            params_section = match.group(2)
            
            transition = Transition(name=function_name, is_async=False)
            
            # Extract parameters: input r0 as address.private;
            param_pattern = r'input\s+(\w+)\s+as\s+([\w\.]+)\s*;'
            param_index = 0
            for param_match in re.finditer(param_pattern, params_section):
                param_var = param_match.group(1)
                param_type_full = param_match.group(2)
                
                # Determine visibility and clean type
                visibility = "public"
                if '.private' in param_type_full:
                    visibility = "private"
                param_type = param_type_full.replace('.private', '').replace('.public', '')
                
                # Create readable parameter name (r0 -> param0, etc.)
                param_name = f"param{param_index}"
                param_index += 1
                
                transition.parameters.append({
                    'name': param_name,
                    'type': param_type,
                    'visibility': visibility
                })
            
            self.contract_info.transitions.append(transition)
        
        # Extract structs from compiled format
        struct_pattern = r'struct\s+(\w+):\s*\n((?:\s+\w+\s+as\s+\w+\s*;\s*\n)+)'
        for match in re.finditer(struct_pattern, content):
            struct_name = match.group(1)
            struct_body = match.group(2)
            
            fields = {}
            field_pattern = r'(\w+)\s+as\s+(\w+)\s*;'
            for field_match in re.finditer(field_pattern, struct_body):
                fields[field_match.group(1)] = field_match.group(2)
            
            self.contract_info.structs.append({
                'name': struct_name,
                'fields': fields
            })
    
    def _analyze_source_leo(self, content: str):
        """Analyze source .leo file format (original implementation)"""
        # Extract program name
        program_match = re.search(r'program\s+(\w+)\.aleo\s*{', content)
        if program_match:
            self.contract_info.program_name = program_match.group(1)
        
        # Extract components
        self._extract_constants(content)
        self._extract_structs(content)
        self._extract_records(content)
        self._extract_mappings(content)
        self._extract_transitions(content)
    
    def _extract_constants(self, content: str):
        """Extract constants from contract"""
        const_pattern = r'const\s+(\w+):\s*(\w+)\s*=\s*([^;]+);'
        matches = re.finditer(const_pattern, content)
        
        for match in matches:
            constant = Constant(
                name=match.group(1),
                type_=match.group(2),
                value=match.group(3).strip()
            )
            self.contract_info.constants.append(constant)
    
    def _extract_structs(self, content: str):
        """Extract structs from contract"""
        struct_pattern = r'struct\s+(\w+)\s*{([^}]+)}'
        matches = re.finditer(struct_pattern, content)
        
        for match in matches:
            struct_name = match.group(1)
            struct_body = match.group(2)
            
            fields = {}
            field_pattern = r'(\w+):\s*(\w+)'
            for field_match in re.finditer(field_pattern, struct_body):
                fields[field_match.group(1)] = field_match.group(2)
            
            self.contract_info.structs.append({
                'name': struct_name,
                'fields': fields
            })
    
    def _extract_records(self, content: str):
        """Extract records from contract"""
        record_pattern = r'record\s+(\w+)\s*{([^}]+)}'
        matches = re.finditer(record_pattern, content)
        
        for match in matches:
            record_name = match.group(1)
            record_body = match.group(2)
            
            record = Record(name=record_name)
            
            # Extract fields
            field_pattern = r'(\w+):\s*(\w+)'
            for field_match in re.finditer(field_pattern, record_body):
                record.fields[field_match.group(1)] = field_match.group(2)
            
            self.contract_info.records.append(record)
    
    def _extract_mappings(self, content: str):
        """Extract mappings from contract"""
        mapping_pattern = r'mapping\s+(\w+):\s*(\w+)\s*=>\s*(\w+);'
        matches = re.finditer(mapping_pattern, content)
        
        for match in matches:
            mapping = Mapping(
                name=match.group(1),
                key_type=match.group(2),
                value_type=match.group(3)
            )
            self.contract_info.mappings.append(mapping)
    
    def _extract_transitions(self, content: str):
        """Extract transitions from contract"""
        # Pattern for async transitions
        async_pattern = r'async\s+transition\s+(\w+)\s*\(([^)]*)\)\s*->\s*([^{]+){'
        # Pattern for regular transitions
        regular_pattern = r'(?<!async\s)transition\s+(\w+)\s*\(([^)]*)\)\s*->\s*([^{]+){'
        
        # Extract async transitions
        for match in re.finditer(async_pattern, content):
            transition = self._parse_transition(match, is_async=True)
            self.contract_info.transitions.append(transition)
        
        # Extract regular transitions
        for match in re.finditer(regular_pattern, content):
            transition = self._parse_transition(match, is_async=False)
            self.contract_info.transitions.append(transition)
    
    def _parse_transition(self, match, is_async: bool) -> Transition:
        """Parse a transition from regex match"""
        name = match.group(1)
        params_str = match.group(2).strip()
        returns_str = match.group(3).strip()
        
        transition = Transition(name=name, is_async=is_async)
        
        # Parse parameters
        if params_str:
            params = params_str.split(',')
            for param in params:
                param = param.strip()
                if param:
                    # Handle visibility modifiers
                    visibility = "private"
                    if param.startswith('public '):
                        visibility = "public"
                        param = param[7:]
                    
                    # Extract parameter name and type
                    parts = param.split(':')
                    if len(parts) == 2:
                        param_name = parts[0].strip()
                        param_type = parts[1].strip()
                        transition.parameters.append({
                            'name': param_name,
                            'type': param_type,
                            'visibility': visibility
                        })
        
        # Parse returns
        if returns_str and returns_str != 'Future':
            # Handle tuple returns
            if returns_str.startswith('(') and returns_str.endswith(')'):
                returns_str = returns_str[1:-1]
                returns = [r.strip() for r in returns_str.split(',')]
                transition.returns = returns
            else:
                transition.returns = [returns_str.strip()]
        
        return transition
    
    def get_contract_summary(self) -> Dict[str, Any]:
        """Get a summary of the analyzed contract"""
        if not self.contract_info:
            return {}
        
        return {
            'program_name': self.contract_info.program_name,
            'num_records': len(self.contract_info.records),
            'num_mappings': len(self.contract_info.mappings),
            'num_transitions': len(self.contract_info.transitions),
            'num_constants': len(self.contract_info.constants),
            'num_structs': len(self.contract_info.structs),
            'transitions': [t.name for t in self.contract_info.transitions]
        } 