"""Integration tests for PR Formatter and V-BOM generation."""
import pytest
from patchforge.delivery.pr_formatter import PRFormatter
from patchforge.models.vulnerability import VulnerabilityLocation
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.formal import FormalInvariant
from patchforge.models.sandbox import SandboxResult


def test_pr_formatter_vbom_generation():
    formatter = PRFormatter()
    state = {
        "cwe_id": "CWE-89",
        "vulnerability": VulnerabilityLocation(
            file_path="app.py",
            start_line=28,
            end_line=28,
            sink_symbol="cursor.execute(query)",
            skull_rating="4_skulls",
        ),
        "ast_slice": ASTContextSlice(
            slice_code="cursor.execute(query)",
            start_line=20,
            end_line=30,
            enclosing_function="get_user",
        ),
        "formal_invariants": FormalInvariant(
            predicate_formula="parameterized == True",
            z3_model_status="VIOLATION_POSSIBLE",
            required_invariants=["MUST_USE_PARAMETERIZED_QUERY"],
        ),
        "sandbox_result": SandboxResult(
            exit_code=0,
            baseline_passed=True,
            reproduction_defended=True,
            stdout="OK",
            stderr="",
            mutation_score=92.5,
            delta_sast_clean=True,
        ),
    }

    pr_body = formatter.format_pr(state)

    assert "## 🎃 PatchForge AI — Autonomous Remediation Notice" in pr_body
    assert "CWE-89" in pr_body
    assert "4_skulls" in pr_body
    assert "MUST_USE_PARAMETERIZED_QUERY" in pr_body
    assert "Verification Bill of Materials (V-BOM)" in pr_body
    assert "92.5%" in pr_body
    assert "⚰️ R.I.P. CWE-89" in pr_body

