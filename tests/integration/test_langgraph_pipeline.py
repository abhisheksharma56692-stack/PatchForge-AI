"""Integration test for LangGraph state machine pipeline."""
import os
import pytest
from patchforge.orchestrator.graph import RemediationPipelineGraph


def test_langgraph_pipeline_execution():
    os.environ["PATCHFORGE_USE_STUBS"] = "true"
    pipeline = RemediationPipelineGraph()

    initial_state = {
        "sarif_raw": {"file_path": "tests/fixtures/sarif/semgrep_cwe89_sqli.sarif.json"},
        "vulnerability": None,
        "cwe_id": "CWE-UNKNOWN",
        "cve_id": None,
        "ast_slice": None,
        "formal_invariants": None,
        "reproduction_test": None,
        "candidate_patch_diff": None,
        "iteration_count": 0,
        "max_iterations": 5,
        "error_feedback_history": [],
        "sandbox_result": None,
        "audit_passed": False,
        "pr_url": None,
        "status": "AWAKENING",
    }

    final_state = pipeline.invoke(initial_state)

    assert final_state["status"] == "TOMBSTONE_READY"
    assert final_state["cwe_id"] == "CWE-89"
    assert final_state["pr_url"] is not None
    assert final_state["ast_slice"] is not None
    assert final_state["formal_invariants"] is not None
    assert final_state["candidate_patch_diff"] is not None

