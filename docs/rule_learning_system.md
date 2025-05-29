# LeoForge Rule Learning System

## Overview

LeoForge includes an intelligent rule learning system that analyzes errors from project generation runs and creates rules to improve future generations. **As of the latest update, rule generation is no longer automatic** - rules are now generated manually via CLI commands to give users more control over the learning process.

## Key Changes

### Manual Rule Generation
- **Automatic rule generation during pipeline execution has been disabled**
- Rules are now generated on-demand using the `leoforge analyze-logs` command
- Only logs with errors that resulted in successful builds are analyzed by default
- This approach reduces noise and focuses on learning from recoverable errors

### Selective Log Analysis
- The system now filters logs to focus on meaningful learning opportunities
- Logs without build errors are ignored (evaluation errors are not considered for rule generation)
- Logs with build errors that never resulted in a successful build are excluded by default
- Only logs with build errors that were eventually resolved are considered for rule generation
- This focuses on concrete compilation issues rather than subjective evaluation concerns

## Components

### 1. **LeoLogger** (`src/services/logger.py`)
Manages error logging and run tracking throughout the project generation process.

**Features:**
- Logs all errors encountered during generation
- Tracks different code versions at each iteration
- Records the resolution path showing how errors were fixed
- Saves logs to JSON files for persistence
- Retrieves recent runs for analysis

**Usage:**
```python
    logger = LeoLogger()
    run_log = logger.start_run("MyProject")
    logger.log_error(iteration_number=1, error_type="build", error_message="Syntax error", code_version=code)
    logger.log_code_version(code)
    logger.log_resolution_step("Fixed syntax error by adding semicolon")
    completed_run = logger.end_run(success=True)
```

### 2. **RuleEngineerAgent** (`src/leoagents/rule_engineer.py`)
An AI agent that analyzes error logs and creates improvement rules.

**Features:**
- Analyzes complete run logs including errors and resolutions
- Identifies patterns in errors and successful fixes
- Creates specific rules for the Architect agent (design phase)
- Creates specific rules for the Code Generator agent (implementation phase)
- Prioritizes rules by importance (1-10 scale)

**Tools:**
- `write_architect_rule`: Creates rules for improving architecture design
- `write_codex_rule`: Creates rules for improving code generation

### 3. **RuleManager** (`src/services/rule_manager.py`)
Manages persistent storage and retrieval of learned rules.

**Features:**
- Saves rules to JSON files for persistence across runs
- Retrieves top rules by priority
- Formats rules for inclusion in agent prompts
- Prevents duplicate rules

**Usage:**
```python
rule_manager = RuleManager()
rule_manager.save_rules(architect_rules, codex_rules)
top_architect_rules = rule_manager.get_architect_rules(limit=5)
rules_prompt = rule_manager.format_rules_for_prompt(top_architect_rules)
```

## Integration with Existing Agents

### Enhanced ArchitectAgent
The Architect agent now includes learned rules in its system prompt:
- Retrieves top 5 architect rules from previous runs
- Applies these rules when designing project architecture
- Helps avoid design patterns that previously led to errors

### Enhanced CodeGeneratorAgent
The Code Generator agent includes learned rules:
- Retrieves top 5 code generation rules
- Applies these rules when generating Leo code
- Avoids code patterns that previously caused compilation errors

## Workflow

1. **During Project Generation:**
   - Every error is logged with context
   - Code versions are tracked at each iteration
   - Resolution steps are recorded

2. **After Run Completion:**
   - The orchestrator **no longer automatically analyzes logs**
   - Logs are saved for later manual analysis
   - **If there are no errors, no analysis is performed**
   - **RuleEngineerAgent analyzes the error logs if present**
   - **Rules are generated based on error patterns and resolutions**

3. **Manual Rule Generation:**
   - Use `leoforge analyze-logs` to analyze specific logs
   - The system filters for logs with errors that resulted in successful builds
   - Rules are generated based on error patterns and resolutions
   - Rules are saved persistently for future use

4. **In Future Runs:**
   - Agents load learned rules from RuleManager
   - Rules are included in agent prompts
   - Agents apply rules to avoid previous mistakes

## New CLI Commands

### `leoforge analyze-logs`
Analyze error logs and generate improvement rules manually.

**Usage:**
```bash
# List available logs (filtered for eligible ones)
leoforge analyze-logs --list

# Analyze a specific log file
leoforge analyze-logs "project_name_uuid.json"

# Interactive mode - select from eligible logs
leoforge analyze-logs

# Include all logs (not just those with recoverable errors)
leoforge analyze-logs --all
```

**Features:**
- Automatically filters for logs with build errors that resulted in successful builds
- Interactive selection from eligible logs
- Detailed analysis summary before rule generation
- Confirmation prompt before generating rules
- Focuses only on compilation/build errors, ignoring evaluation errors

### `leoforge rules`
Manage and view generated improvement rules.

**Usage:**
```bash
# List all rules
leoforge rules

# List only architect rules
leoforge rules --type architect

# List only code generator rules  
leoforge rules --type codex

# Export rules to a file
leoforge rules --export my_rules.json

# Clear all rules (with confirmation)
leoforge rules --clear
```

**Features:**
- Tabular display of rules with priorities and tags
- Detailed view of top rules
- Export functionality for backup/sharing
- Safe rule clearing with confirmation

## Handling Successful Runs Without Errors

When a run succeeds without errors, the system simply logs the success and moves on. No rule analysis is performed because there are no errors to learn from. The focus is exclusively on learning from failures and errors to prevent them in future runs.

## Data Models

### ErrorLog
```python
@dataclass
class ErrorLog:
    timestamp: datetime
    iteration_number: int
    error_type: str  # compilation, evaluation, build
    error_message: str
    code_version: str
    context: Optional[str]
```

### RunLog
```python
@dataclass
class RunLog:
    run_id: str
    project_name: str
    start_time: datetime
    end_time: Optional[datetime]
    success: bool
    error_logs: List[ErrorLog]
    code_versions: List[str]
    resolution_path: List[str]
```

### LeoRule
```python
class LeoRule(BaseModel):
    rule_id: str
    rule_type: RuleType  # ARCHITECT or CODEX
    title: str
    description: str
    pattern: str  # Pattern to avoid
    solution: str  # Recommended solution
    examples: List[str]
    priority: int  # 1-10, 10 being most important
    tags: List[str]
    created_from_errors: List[str]
```

## Storage

- **Logs**: Stored in `logs/` directory as JSON files
- **Rules**: Stored in `rules/leo_rules.json`

## Example Rule

```json
{
    "rule_id": "rule_001",
    "rule_type": "codex",
    "title": "Avoid mapping operations in async transitions",
    "description": "Mappings cannot be accessed directly in async transitions in Leo",
    "pattern": "Using Mapping.get() or Mapping.set() inside async transition",
    "solution": "Move mapping operations to a separate finalize function or redesign to use records",
    "examples": [
        "async transition transfer() { let balance = balances.get(sender); }",
        "Use records to track state instead of mappings in async contexts"
    ],
    "priority": 9,
    "tags": ["async", "mapping", "compilation-error"],
    "created_from_errors": ["error_log_123", "error_log_456"]
}
```

## Benefits

1. **Continuous Improvement**: The system learns from every error
2. **Error Prevention**: Common mistakes are avoided in future runs
3. **Knowledge Persistence**: Learning persists across sessions
4. **Transparent Learning**: Rules are human-readable and can be reviewed
5. **Prioritized Application**: Most important rules are applied first

## Future Enhancements

- Rule versioning and evolution
- Rule effectiveness tracking
- Cross-project rule sharing
- Rule conflict resolution
- Manual rule editing interface 