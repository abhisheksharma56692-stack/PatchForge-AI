"""Seeds realistic static vulnerability findings and graveyard tombstones if empty."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from patchforge.db.models import (
    VulnerabilityModel,
    RemediationRunModel,
    CandidatePatchModel,
    TestResultModel,
)


def seed_initial_data(db: Session) -> None:
    """Populates initial DevSecOps findings and cemetery tombstones."""
    # Check if data already exists
    if db.query(VulnerabilityModel).count() > 0:
        return

    now = datetime.utcnow()

    # 1. Active Vulnerabilities in the Crypt
    v1 = VulnerabilityModel(
        id="vuln-cwe89-01",
        cwe_id="CWE-89",
        cve_id="CVE-2026-3819",
        title="SQL Injection in User Authentication Endpoint",
        scanner_name="Semgrep v1.68",
        rule_id="python.django.security.injection.sql.sql-injection",
        file_path="backend/views/user.py",
        start_line=42,
        end_line=44,
        start_col=4,
        end_col=58,
        sink_symbol="cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")",
        severity="CRITICAL",
        skull_count=5,
        status="OPEN",
        slice_line_count=28,
        created_at=now - timedelta(hours=1),
    )

    v2 = VulnerabilityModel(
        id="vuln-cwe22-02",
        cwe_id="CWE-22",
        cve_id="CVE-2026-4012",
        title="Improper Limitation of a Pathname to a Restricted Directory",
        scanner_name="Bandit v1.7.5",
        rule_id="python.bandit.B108.path_traversal",
        file_path="backend/handlers/file_storage.py",
        start_line=89,
        end_line=91,
        sink_symbol='open(os.path.join(BASE_DIR, filename), "rb")',
        severity="HIGH",
        skull_count=4,
        status="IN_PROGRESS",
        slice_line_count=32,
        created_at=now - timedelta(hours=3),
    )

    v3 = VulnerabilityModel(
        id="vuln-cwe79-03",
        cwe_id="CWE-79",
        cve_id="CVE-2026-2911",
        title="Cross-Site Scripting (XSS) via Unsanitized Template Output",
        scanner_name="Snyk Code",
        rule_id="javascript.express.security.xss",
        file_path="frontend/templates/profile.html",
        start_line=115,
        end_line=116,
        sink_symbol="element.innerHTML = user_bio_raw",
        severity="MEDIUM",
        skull_count=3,
        status="OPEN",
        slice_line_count=18,
        created_at=now - timedelta(hours=5),
    )

    v4 = VulnerabilityModel(
        id="vuln-cwe787-04",
        cwe_id="CWE-787",
        cve_id="CVE-2026-5510",
        title="Out-of-bounds Write in String Buffer Tokenizer",
        scanner_name="CodeQL",
        rule_id="cpp.buffer-overflow.unbounded-copy",
        file_path="native/tokenizer.c",
        start_line=164,
        end_line=166,
        sink_symbol="strcpy(buffer + offset, input)",
        severity="CRITICAL",
        skull_count=5,
        status="OPEN",
        slice_line_count=42,
        created_at=now - timedelta(hours=8),
    )

    # 2. Resolved Historical Vulnerabilities (for Graveyard Tombstones)
    v_res1 = VulnerabilityModel(
        id="vuln-resolved-01",
        cwe_id="CWE-89",
        cve_id="CVE-2026-1102",
        title="SQL Injection in Account Search Query",
        scanner_name="Semgrep",
        rule_id="python.django.security.injection.sql",
        file_path="backend/routes/accounts.py",
        start_line=50,
        end_line=52,
        sink_symbol="cursor.execute(raw_query)",
        severity="CRITICAL",
        skull_count=5,
        status="RESOLVED",
        created_at=now - timedelta(days=2),
    )

    v_res2 = VulnerabilityModel(
        id="vuln-resolved-02",
        cwe_id="CWE-22",
        cve_id="CVE-2026-1188",
        title="Path Traversal via User File Download Route",
        scanner_name="Bandit",
        rule_id="python.bandit.path_traversal",
        file_path="backend/services/storage_service.py",
        start_line=34,
        end_line=36,
        sink_symbol="send_file(user_path)",
        severity="HIGH",
        skull_count=4,
        status="RESOLVED",
        created_at=now - timedelta(days=3),
    )

    v_res3 = VulnerabilityModel(
        id="vuln-resolved-03",
        cwe_id="CWE-79",
        cve_id="CVE-2026-1204",
        title="Stored XSS in Comment Render Field",
        scanner_name="Snyk",
        rule_id="javascript.stored_xss",
        file_path="web/controllers/comments.js",
        start_line=82,
        end_line=83,
        sink_symbol="res.render('comments', { text: raw_input })",
        severity="MEDIUM",
        skull_count=3,
        status="RESOLVED",
        created_at=now - timedelta(days=4),
    )

    v_res4 = VulnerabilityModel(
        id="vuln-resolved-04",
        cwe_id="CWE-502",
        cve_id="CVE-2026-1309",
        title="Deserialization of Untrusted Data via Python Pickle",
        scanner_name="Semgrep",
        rule_id="python.lang.security.deserialization.pickle",
        file_path="workers/task_queue.py",
        start_line=29,
        end_line=30,
        sink_symbol="pickle.loads(payload)",
        severity="HIGH",
        skull_count=4,
        status="RESOLVED",
        created_at=now - timedelta(days=5),
    )

    db.add_all([v1, v2, v3, v4, v_res1, v_res2, v_res3, v_res4])
    db.commit()

    # 3. Create Corresponding Runs & Graveyard Tombstones
    r1 = RemediationRunModel(
        id="run-grave-001",
        vulnerability_id=v_res1.id,
        repo_path="backend/routes/accounts.py",
        remediation_branch="patchforge/remediate-cwe-89-104",
        iteration_count=1,
        status="SUCCEEDED",
        baseline_tests_passed=True,
        reproduction_defended=True,
        mutation_score=93.8,
        delta_sast_clean=True,
        duration_seconds=135.0,
        pr_url="https://github.com/patchforge-org/demo-repo/pull/104",
        pr_number=104,
        commit_sha="a9f24c08e1",
        tombstone_inscription="⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge via Parametric Binding",
        completed_at=now - timedelta(days=2),
    )

    r2 = RemediationRunModel(
        id="run-grave-002",
        vulnerability_id=v_res2.id,
        repo_path="backend/services/storage_service.py",
        remediation_branch="patchforge/remediate-cwe-22-103",
        iteration_count=2,
        status="SUCCEEDED",
        baseline_tests_passed=True,
        reproduction_defended=True,
        mutation_score=91.2,
        delta_sast_clean=True,
        duration_seconds=158.0,
        pr_url="https://github.com/patchforge-org/demo-repo/pull/103",
        pr_number=103,
        commit_sha="b3d81f72c4",
        tombstone_inscription="⚰️ R.I.P. CWE-22 (Path Traversal) — Neutralized by PatchForge via Canonical Path Validation",
        completed_at=now - timedelta(days=3),
    )

    r3 = RemediationRunModel(
        id="run-grave-003",
        vulnerability_id=v_res3.id,
        repo_path="web/controllers/comments.js",
        remediation_branch="patchforge/remediate-cwe-79-102",
        iteration_count=1,
        status="SUCCEEDED",
        baseline_tests_passed=True,
        reproduction_defended=True,
        mutation_score=96.0,
        delta_sast_clean=True,
        duration_seconds=112.0,
        pr_url="https://github.com/patchforge-org/demo-repo/pull/102",
        pr_number=102,
        commit_sha="c7e19924a5",
        tombstone_inscription="⚰️ R.I.P. CWE-79 (Stored XSS) — Neutralized by PatchForge via HTML Entity Encoding",
        completed_at=now - timedelta(days=4),
    )

    r4 = RemediationRunModel(
        id="run-grave-004",
        vulnerability_id=v_res4.id,
        repo_path="workers/task_queue.py",
        remediation_branch="patchforge/remediate-cwe-502-101",
        iteration_count=2,
        status="SUCCEEDED",
        baseline_tests_passed=True,
        reproduction_defended=True,
        mutation_score=89.5,
        delta_sast_clean=True,
        duration_seconds=174.0,
        pr_url="https://github.com/patchforge-org/demo-repo/pull/101",
        pr_number=101,
        commit_sha="d4a32981f6",
        tombstone_inscription="⚰️ R.I.P. CWE-502 (Insecure Deserialization) — Neutralized by PatchForge via Safe JSON Schema",
        completed_at=now - timedelta(days=5),
    )

    db.add_all([r1, r2, r3, r4])
    db.commit()

