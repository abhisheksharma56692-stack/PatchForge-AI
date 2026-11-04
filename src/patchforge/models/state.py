"""LangGraph central state schema for the remediation pipeline."""
from typing import TypedDict, List, Dict, Optional, Any
from patchforge.models.vulnerability import VulnerabilityLocation
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.formal import FormalInvariant
from patchforge.models.agents import TestArtifact
from patchforge.models.sandbox import SandboxResult


class RemediationGraphState(TypedDict):
    """Central state machine graph schema flowing through LangGraph nodes."""
    sarif_raw: Dict[str, Any]
    vulnerability: VulnerabilityLocation
    cwe_id: str
    cve_id: Optional[str]
    ast_slice: ASTContextSlice
    formal_invariants: FormalInvariant
    reproduction_test: Optional[TestArtifact]
    candidate_patch_diff: Optional[str]
    iteration_count: int
    max_iterations: int
    error_feedback_history: List[str]
    sandbox_result: Optional[SandboxResult]
    audit_passed: bool
    pr_url: Optional[str]
    # Halloween-aligned status values:
    # "AWAKENING", "DISSECTING", "CONJURING", "DUELING", "TOMBSTONE_READY", "HAUNTED_FAIL"
    status: str

