"""Agent Gamma: Anti-Tamper Auditor."""
import re
from typing import List
from patchforge.models.agents import PatchCandidate, AuditVerdict
from patchforge.models.slicing import ASTContextSlice


class AntiTamperAuditor:
    """
    Agent Gamma (Auditor): Deterministically inspects candidate patches to ensure
    they do not tamper with test suites, remove assertions, or alter scanner configs.
    """

    FORBIDDEN_FILES = [
        r"tests/.*",
        r"test/.*",
        r".*\.test\.(js|ts|py)",
        r".*_test\.(py|go)",
        r"\.semgrep\.ya?ml",
        r"\.bandit",
        r"\.snyk",
        r"sonar-project\.properties",
        r"\.eslintrc.*",
    ]

    def audit(self, patch: PatchCandidate, allowed_slice: ASTContextSlice) -> AuditVerdict:
        """Audits a unified diff against anti-tamper security invariants."""
        violations: List[str] = []
        diff_text = patch.diff_content

        # 1. Check touched file paths
        file_headers = re.findall(r"^(?:---|\+\+\+)\s+[ab]/(.*)$", diff_text, re.MULTILINE)
        for filepath in file_headers:
            for pattern in self.FORBIDDEN_FILES:
                if re.match(pattern, filepath, re.IGNORECASE):
                    violations.append(
                        f"TAMPER_VIOLATION: Patch attempts to modify forbidden security/test file '{filepath}'"
                    )

        # 2. Check for removal of test assertions
        # Look for deleted lines starting with '-' (not '---') that contain assertions
        deleted_lines = re.findall(r"^-(?!--)\s*(.*)$", diff_text, re.MULTILINE)
        for line in deleted_lines:
            line_clean = line.strip()
            if re.match(r"^assert\b", line_clean) or "expect(" in line_clean or "assert." in line_clean:
                violations.append(
                    f"TAMPER_VIOLATION: Patch deletes test assertion: '{line_clean}'"
                )

        # 3. Check AST slice boundary
        # Extract modified lines from diff hunk headers: @@ -start,count +start,count @@
        hunks = re.findall(r"@@\s*-(\d+)(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s*@@", diff_text)
        slice_start = allowed_slice.start_line
        slice_end = allowed_slice.end_line
        
        # Buffer tolerance for surrounding context in hunks (e.g. 5 lines)
        tolerance = 10
        boundary_start = max(1, slice_start - tolerance)
        boundary_end = slice_end + tolerance

        for orig_line_str, new_line_str in hunks:
            orig_line = int(orig_line_str)
            if orig_line < boundary_start or orig_line > boundary_end:
                violations.append(
                    f"BOUNDARY_VIOLATION: Patch modifies line {orig_line} which is outside allowed AST slice boundary [{slice_start}, {slice_end}]"
                )

        approved = len(violations) == 0
        rejection_reason = "; ".join(violations) if not approved else None

        return AuditVerdict(
            approved=approved,
            violations=violations,
            rejection_reason=rejection_reason,
            tamper_check_passed=approved,
            boundary_check_passed=approved,
        )

