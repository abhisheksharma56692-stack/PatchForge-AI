"""Mock agent stubs (Alpha, Beta, Gamma, Reflection) for Member 2 development."""
from typing import Optional
from patchforge.models.vulnerability import VulnerabilityReport
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.formal import FormalInvariant
from patchforge.models.agents import (
    TestArtifact,
    PatchCandidate,
    AuditVerdict,
    ReflectionFeedback,
)
from patchforge.models.sandbox import SandboxResult


class TestSynthesizerAgent:
    """Mock Agent Alpha generating reproduction test artifact."""
    __test__ = False

    def __init__(self, llm_client=None):
        self.llm = llm_client

    def synthesize(self, vuln: VulnerabilityReport, slice_context: ASTContextSlice) -> TestArtifact:
        return TestArtifact(
            test_file_path="tests/test_cwe89_reproduction.py",
            test_code=(
                "import pytest\n"
                "def test_sqli_poc():\n"
                "    payload = \"' OR '1'='1\"\n"
                "    assert payload != ''\n"
            ),
            test_type="reproduction_poc",
            target_cwe=vuln.cwe_id,
            execution_command="pytest tests/test_cwe89_reproduction.py",
        )


class PatchSynthesizerAgent:
    """Mock Agent Beta generating unified diff."""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    def synthesize(
        self,
        slice_context: ASTContextSlice,
        invariants: FormalInvariant,
        poc_test: TestArtifact,
        feedback: Optional[ReflectionFeedback] = None,
    ) -> PatchCandidate:
        diff_text = (
            "--- a/app.py\n"
            "+++ b/app.py\n"
            "@@ -25,4 +25,4 @@\n"
            "-    query = 'SELECT id, username FROM users WHERE username = ' + username\n"
            "-    cursor.execute(query)\n"
            "+    query = 'SELECT id, username FROM users WHERE username = ?'\n"
            "+    cursor.execute(query, (username,))\n"
        )
        return PatchCandidate(
            diff_content=diff_text,
            target_file="app.py",
            explanation="Parameterized SQL query implemented to neutralize CWE-89 injection.",
            tombstone_inscription="⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge AI",
            model_name="mock-claude-3-5-sonnet",
        )


class AntiTamperAuditor:
    """Mock Agent Gamma approving compliant diffs."""

    def audit(self, patch: PatchCandidate, allowed_slice: ASTContextSlice) -> AuditVerdict:
        return AuditVerdict(
            approved=True,
            violations=[],
            rejection_reason=None,
            tamper_check_passed=True,
            boundary_check_passed=True,
        )


class ReflectionEngine:
    """Mock Reflection engine providing structured critique."""

    def critique(self, sandbox_result: SandboxResult, iteration: int) -> ReflectionFeedback:
        return ReflectionFeedback(
            iteration=iteration,
            failure_summary="Test assertion failed during reproduction check",
            actionable_critique="Ensure parameter tuple is properly wrapped with (username,)",
            failed_tests=["test_sqli_poc"],
            compiler_errors=[],
            stack_trace_snippet=sandbox_result.stderr[:500] if sandbox_result.stderr else None,
        )

