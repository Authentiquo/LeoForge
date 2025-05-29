"""
Logger Service - Manages error logging and run tracking for LeoForge
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import uuid

from src.models import ErrorLog, RunLog, BuildResult, EvaluationResult, GeneratedCode


class LeoLogger:
    """Service for logging errors and tracking project generation runs"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_run: Optional[RunLog] = None
        
    def start_run(self, project_name: str) -> RunLog:
        """Start logging a new run"""
        run_id = str(uuid.uuid4())
        self.current_run = RunLog(
            run_id=run_id,
            project_name=project_name,
            start_time=datetime.now()
        )
        return self.current_run
    
    def log_error(self, 
                  iteration_number: int,
                  error_type: str,
                  error_message: str,
                  code_version: str,
                  context: Optional[str] = None):
        """Log an error during the run"""
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        error_log = ErrorLog(
            timestamp=datetime.now(),
            iteration_number=iteration_number,
            error_type=error_type,
            error_message=error_message,
            code_version=code_version,
            context=context
        )
        
        self.current_run.error_logs.append(error_log)
    
    def log_code_version(self, code: str):
        """Log a code version generated during the run"""
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        self.current_run.code_versions.append(code)
    
    def log_resolution_step(self, step: str):
        """Log a step in the resolution path"""
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        self.current_run.resolution_path.append(step)
    
    def log_build_errors(self, iteration_number: int, build_result: BuildResult, code: str):
        """Log errors from a build attempt"""
        if build_result.errors:
            for error in build_result.errors:
                self.log_error(
                    iteration_number=iteration_number,
                    error_type="build",
                    error_message=error,
                    code_version=code,
                    context=f"Build status: {build_result.status.value}"
                )
    
    def log_evaluation_issues(self, iteration_number: int, evaluation: EvaluationResult, code: str):
        """Log issues from code evaluation"""
        if evaluation.has_errors:
            # Log missing features
            for feature in evaluation.missing_features:
                self.log_error(
                    iteration_number=iteration_number,
                    error_type="evaluation",
                    error_message=f"Missing feature: {feature}",
                    code_version=code,
                    context=f"Evaluation score: {evaluation.score}"
                )
            
            # Log security issues
            for issue in evaluation.security_issues:
                self.log_error(
                    iteration_number=iteration_number,
                    error_type="evaluation",
                    error_message=f"Security issue: {issue}",
                    code_version=code,
                    context="Security concern"
                )
    
    def end_run(self, success: bool) -> RunLog:
        """End the current run and save logs"""
        if not self.current_run:
            raise ValueError("No active run to end.")
        
        self.current_run.end_time = datetime.now()
        self.current_run.success = success
        
        # Save to file
        self._save_run_log(self.current_run)
        
        completed_run = self.current_run
        self.current_run = None
        return completed_run
    
    def _save_run_log(self, run_log: RunLog):
        """Save run log to file"""
        filename = f"{run_log.project_name}_{run_log.run_id}.json"
        filepath = self.log_dir / filename
        
        # Convert to dict for JSON serialization
        log_data = {
            "run_id": run_log.run_id,
            "project_name": run_log.project_name,
            "start_time": run_log.start_time.isoformat(),
            "end_time": run_log.end_time.isoformat() if run_log.end_time else None,
            "success": run_log.success,
            "error_logs": [
                {
                    "timestamp": log.timestamp.isoformat(),
                    "iteration_number": log.iteration_number,
                    "error_type": log.error_type,
                    "error_message": log.error_message,
                    "context": log.context
                }
                for log in run_log.error_logs
            ],
            "code_versions": run_log.code_versions,
            "resolution_path": run_log.resolution_path
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_recent_runs(self, limit: int = 10) -> List[RunLog]:
        """Get recent run logs for analysis"""
        log_files = sorted(self.log_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:limit]
        
        runs = []
        for file in log_files:
            with open(file, 'r') as f:
                data = json.load(f)
                
            # Reconstruct RunLog from JSON
            run_log = RunLog(
                run_id=data["run_id"],
                project_name=data["project_name"],
                start_time=datetime.fromisoformat(data["start_time"]),
                end_time=datetime.fromisoformat(data["end_time"]) if data["end_time"] else None,
                success=data["success"]
            )
            
            # Reconstruct error logs
            for error_data in data.get("error_logs", []):
                error_log = ErrorLog(
                    timestamp=datetime.fromisoformat(error_data["timestamp"]),
                    iteration_number=error_data["iteration_number"],
                    error_type=error_data["error_type"],
                    error_message=error_data["error_message"],
                    code_version="",  # Not stored in JSON for space
                    context=error_data.get("context")
                )
                run_log.error_logs.append(error_log)
            
            run_log.code_versions = data.get("code_versions", [])
            run_log.resolution_path = data.get("resolution_path", [])
            
            runs.append(run_log)
        
        return runs 
    
    def load_run_log(self, filename: str) -> Optional[RunLog]:
        """Load a specific run log by filename"""
        # Handle both with and without .json extension
        if not filename.endswith('.json'):
            filename += '.json'
            
        filepath = self.log_dir / filename
        
        if not filepath.exists():
            return None
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Reconstruct RunLog from JSON
            run_log = RunLog(
                run_id=data["run_id"],
                project_name=data["project_name"],
                start_time=datetime.fromisoformat(data["start_time"]),
                end_time=datetime.fromisoformat(data["end_time"]) if data["end_time"] else None,
                success=data["success"]
            )
            
            # Reconstruct error logs with full code versions
            for error_data in data.get("error_logs", []):
                error_log = ErrorLog(
                    timestamp=datetime.fromisoformat(error_data["timestamp"]),
                    iteration_number=error_data["iteration_number"],
                    error_type=error_data["error_type"],
                    error_message=error_data["error_message"],
                    code_version="",  # Will be populated from code_versions
                    context=error_data.get("context")
                )
                run_log.error_logs.append(error_log)
            
            # Restore code versions to error logs
            code_versions = data.get("code_versions", [])
            for error_log in run_log.error_logs:
                if error_log.iteration_number <= len(code_versions):
                    error_log.code_version = code_versions[error_log.iteration_number - 1]
            
            run_log.code_versions = code_versions
            run_log.resolution_path = data.get("resolution_path", [])
            
            return run_log
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error loading log file {filename}: {e}")
            return None 