"""Active vulnerabilities crypt endpoint."""
from typing import List
from fastapi import APIRouter
from patchforge.api.schemas import VulnerabilityItem

router = APIRouter(prefix="/api/vulns", tags=["vulnerabilities"])


@router.get("", response_model=List[VulnerabilityItem])
def get_vulnerabilities():
    """Returns detected vulnerabilities in the Crypt with skull ratings."""
    return [
        VulnerabilityItem(
            finding_id="semgrep-cwe89-01",
            cwe_id="CWE-89",
            title="SQL Injection in user authentication",
            severity="HIGH",
            skull_rating="4_skulls",
            file_path="backend/views/user.py",
            start_line=28,
            scanner="semgrep",
            status="AWAKENING",
            exposure_age_hours=0.5,
        ),
        VulnerabilityItem(
            finding_id="bandit-cwe22-02",
            cwe_id="CWE-22",
            title="Path Traversal in document download",
            severity="CRITICAL",
            skull_rating="5_skulls",
            file_path="routes/download.py",
            start_line=15,
            scanner="bandit",
            status="CONJURING",
            exposure_age_hours=1.8,
        ),
        VulnerabilityItem(
            finding_id="snyk-cwe79-03",
            cwe_id="CWE-79",
            title="Cross-Site Scripting (XSS) in greeting view",
            severity="MEDIUM",
            skull_rating="3_skulls",
            file_path="frontend/server.js",
            start_line=22,
            scanner="snyk",
            status="DUELING",
            exposure_age_hours=3.2,
        ),
    ]

