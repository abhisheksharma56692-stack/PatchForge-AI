"""Unit tests for Agent Beta (Patch Synthesizer)."""
import pytest
from unittest.mock import MagicMock
from patchforge.agents.patch_synthesizer import PatchSynthesizerAgent
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.formal import FormalInvariant
from patchforge.models.agents import TestArtifact, ReflectionFeedback


def test_agent_beta_patch_synthesis():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = (
        "Here is the synthesized minimal unified diff:\n"
        "```diff\n"
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -27,3 +27,3 @@\n"
        "-    query = 'SELECT * FROM users WHERE username = ' + username\n"
        "-    cursor.execute(query)\n"
        "+    query = 'SELECT * FROM users WHERE username = ?'\n"
        "+    cursor.execute(query, (username,))\n"
        "```\n"
        "⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge AI\n"
    )

    agent = PatchSynthesizerAgent(llm_client=mock_llm)
    ast_slice = ASTContextSlice(
        slice_code="query = 'SELECT * FROM users WHERE username = ' + username\ncursor.execute(query)",
        start_line=27,
        end_line=29,
        language="python",
    )
    invariants = FormalInvariant(
        predicate_formula="parameterized == True",
        z3_model_status="VIOLATION_POSSIBLE",
        required_invariants=["MUST_USE_PARAMETERIZED_QUERY"],
    )
    poc = TestArtifact(
        test_file_path="tests/test_sqli.py",
        test_code="def test_sqli(): pass",
        target_cwe="CWE-89",
    )

    patch = agent.synthesize(ast_slice, invariants, poc)

    assert "--- a/app.py" in patch.diff_content
    assert "+++ b/app.py" in patch.diff_content
    assert "cursor.execute(query, (username,))" in patch.diff_content
    assert "⚰️ R.I.P." in patch.tombstone_inscription


def test_agent_beta_with_reflection_feedback():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "--- a/app.py\n+++ b/app.py\n@@ -27,1 +27,1 @@\n"
    agent = PatchSynthesizerAgent(llm_client=mock_llm)

    ast_slice = ASTContextSlice(slice_code="x = 1", start_line=25, end_line=30)
    invariants = FormalInvariant(predicate_formula="x > 0", z3_model_status="UNCONDITIONALLY_SAFE")
    poc = TestArtifact(test_file_path="t.py", test_code="pass", target_cwe="CWE-89")
    feedback = ReflectionFeedback(
        iteration=1,
        failure_summary="TypeError occurred",
        actionable_critique="Fix parameter tuple",
    )

    patch = agent.synthesize(ast_slice, invariants, poc, feedback=feedback)
    assert patch is not None
    # Verify feedback was included in user prompt
    _, kwargs = mock_llm.generate.call_args
    assert "TypeError occurred" in kwargs["user"]

