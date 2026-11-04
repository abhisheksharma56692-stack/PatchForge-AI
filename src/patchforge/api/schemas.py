"""Pydantic schemas for the Halloween dashboard REST and WebSocket APIs."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    """Overall operations summary metrics."""
    total_vulnerabilities: int = 12
    open_skulls: int = 3
    in_progress_bats: int = 2
    remediated_ghosts: int = 7
    mean_time_to_remediate_sec: float = 184.5  # ~3 minutes vs enterprise 60 days!
    pipeline_health_percent: float = 98.5
    active_runs: int = 1


class VulnerabilityItem(BaseModel):
    """Active vulnerability finding in the Crypt."""
    finding_id: str
    cwe_id: str
    title: str
    severity: str
    skull_rating: str  # "1_skull" to "5_skulls"
    file_path: str
    start_line: int
    scanner: str
    status: str
    exposure_age_hours: float = 1.2


class RunRecord(BaseModel):
    """Historical remediation run record."""
    run_id: str
    cwe_id: str
    status: str
    duration: float
    pr_url: str
    timestamp: int
    tombstone_inscription: Optional[str] = None


class PipelineEvent(BaseModel):
    """WebSocket state transition event."""
    event: str
    step: str
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)

