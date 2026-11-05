"""Pydantic schemas for the Halloween dashboard REST and WebSocket APIs."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    """Overall operations summary metrics for Haunted Home."""
    total_vulnerabilities: int = 18
    open_skulls: int = 4
    in_progress_bats: int = 2
    remediated_ghosts: int = 12
    mean_time_to_remediate_sec: float = 142.5
    pipeline_health_percent: float = 99.4
    aws_bedrock_tokens_used: int = 124890
    sandbox_containers_spawned: int = 36
    active_runs: int = 2


class VulnerabilityItem(BaseModel):
    """Vulnerability finding item in the Crypt."""
    id: str
    finding_id: Optional[str] = None
    cwe_id: str
    cve_id: Optional[str] = None
    title: str
    severity: str
    skulls: int = 4
    skull_rating: str = "4_skulls"
    file_path: str
    line_number: int = 42
    start_line: int = 42
    sink_symbol: str = "cursor.execute(query)"
    scanner: str = "Semgrep"
    status: str = "OPEN"
    slice_line_count: int = 28
    exposure_age_hours: float = 1.5


class RunRecord(BaseModel):
    """Historical remediation run / Graveyard tombstone record."""
    id: str
    run_id: Optional[str] = None
    cwe_id: str = "CWE-89"
    title: str = "SQL Injection in User Authentication"
    file_path: str = "backend/views/user.py"
    status: str = "TOMBSTONE_READY"
    duration: float = 135.0
    mttr_seconds: float = 135.0
    pr_url: str = "https://github.com/patchforge-org/demo-repo/pull/104"
    pr_number: int = 104
    mutation_score: float = 92.4
    timestamp: int = 0
    resolved_at: Optional[str] = None
    tombstone_inscription: Optional[str] = None


class TriggerRunRequest(BaseModel):
    """Request payload to initiate autonomous remediation."""
    vulnerability_id: Optional[str] = None
    file: Optional[str] = None
    repo_path: Optional[str] = None


class TriggerRunResponse(BaseModel):
    """Response returned upon dispatching a remediation pipeline."""
    status: str
    run_id: str
    message: str
    vulnerability_id: Optional[str] = None


class PipelineEvent(BaseModel):
    """WebSocket state transition event envelope."""
    event: str
    step: Optional[str] = None
    status: Optional[str] = None
    timestamp: Optional[str] = None
    run_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    data: Dict[str, Any] = Field(default_factory=dict)
