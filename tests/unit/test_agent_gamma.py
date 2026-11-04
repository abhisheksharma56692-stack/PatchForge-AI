"""Unit tests for Agent Gamma (Anti-Tamper Auditor)."""
import pytest
from patchforge.agents.auditor import AntiTamperAuditor
from patchforge.models.agents import PatchCandidate
from patchforge.models.slicing import ASTContextSlice


def test_auditor_approves_valid_patch():
    auditor = AntiTamperAuditor()
    patch = PatchCandidate(
        diff_content=(
            "--- a/app.py\n"
            "+++ b/app.py\n"
            "@@ -25,2 +25,2 @@\n"
            "-    query = 'SELECT * FROM users WHERE username = ' + username\n"
            "+    query = 'SELECT * FROM users WHERE username = ?'\n"
        ),
        target_file="app.py",
    )
    allowed_slice = ASTContextSlice(
        slice_code="dummy",
        start_line=20,
        end_line=30,
    )
    verdict = auditor.audit(patch, allowed_slice)
    assert verdict.approved is True
    assert len(verdict.violations) == 0


def test_auditor_rejects_test_file_modification():
    auditor = AntiTamperAuditor()
    patch = PatchCandidate(
        diff_content=(
            "--- a/tests/test_sqli.py\n"
            "+++ b/tests/test_sqli.py\n"
            "@@ -10,1 +10,1 @@\n"
            "-    assert res.status_code == 200\n"
            "+    pass\n"
        ),
        target_file="tests/test_sqli.py",
    )
    allowed_slice = ASTContextSlice(slice_code="dummy", start_line=1, end_line=50)
    verdict = auditor.audit(patch, allowed_slice)
    assert verdict.approved is False
    assert any("forbidden security/test file" in v for v in verdict.violations)


def test_auditor_rejects_scanner_config_modification():
    auditor = AntiTamperAuditor()
    patch = PatchCandidate(
        diff_content=(
            "--- a/.semgrep.yml\n"
            "+++ b/.semgrep.yml\n"
            "@@ -1,3 +1,0 @@\n"
        ),
        target_file=".semgrep.yml",
    )
    allowed_slice = ASTContextSlice(slice_code="dummy", start_line=1, end_line=50)
    verdict = auditor.audit(patch, allowed_slice)
    assert verdict.approved is False
    assert any("forbidden security/test file" in v for v in verdict.violations)


def test_auditor_rejects_assertion_deletion():
    auditor = AntiTamperAuditor()
    patch = PatchCandidate(
        diff_content=(
            "--- a/app.py\n"
            "+++ b/app.py\n"
            "@@ -25,2 +25,1 @@\n"
            "-    assert len(users) > 0\n"
            "+    return users\n"
        ),
        target_file="app.py",
    )
    allowed_slice = ASTContextSlice(slice_code="dummy", start_line=20, end_line=30)
    verdict = auditor.audit(patch, allowed_slice)
    assert verdict.approved is False
    assert any("deletes test assertion" in v for v in verdict.violations)


def test_auditor_rejects_out_of_boundary_patch():
    auditor = AntiTamperAuditor()
    patch = PatchCandidate(
        diff_content=(
            "--- a/app.py\n"
            "+++ b/app.py\n"
            "@@ -95,2 +95,2 @@\n"
            "-    old_code()\n"
            "+    new_code()\n"
        ),
        target_file="app.py",
    )
    # Allowed slice is lines 10 to 25
    allowed_slice = ASTContextSlice(slice_code="dummy", start_line=10, end_line=25)
    verdict = auditor.audit(patch, allowed_slice)
    assert verdict.approved is False
    assert any("outside allowed AST slice boundary" in v for v in verdict.violations)

