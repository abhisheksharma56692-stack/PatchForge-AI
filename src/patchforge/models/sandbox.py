"""Sandbox execution and verification models."""
from typing import List
from pydantic import BaseModel, Field


class SandboxResult(BaseModel):
    """Result of sandbox evaluation for a patch candidate."""
    exit_code: int
    baseline_passed: bool
    reproduction_defended: bool
    stdout: str
    stderr: str
    mutation_score: float = 0.0
    delta_sast_clean: bool = False
    execution_time_sec: float = 0.0


class MutationReport(BaseModel):
    """Mutation testing result for patch verification."""
    total_mutants: int
    killed_mutants: int
    survived_mutants: int
    equivalent_mutants: int = 0
    mutation_score: float
    passed_threshold: bool  # >= 85%


class DeltaSASTReport(BaseModel):
    """Delta-SAST re-scan verification report."""
    original_finding_cleared: bool
    new_findings_count: int
    clean: bool
    diagnostics: List[str] = Field(default_factory=list)

