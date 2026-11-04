"""Unit tests for SARIF ingestion and normalization."""
import os
import pytest
from patchforge.ingestion.sarif_parser import (
    parse_sarif_file,
    validate_sarif_schema,
    extract_findings,
    normalize_location,
)
from patchforge.ingestion.scanner_adapters.semgrep import SemgrepAdapter
from patchforge.ingestion.scanner_adapters.snyk import SnykAdapter
from patchforge.ingestion.scanner_adapters.bandit import BanditAdapter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEMGREP_FIXTURE = os.path.join(BASE_DIR, "tests", "fixtures", "sarif", "semgrep_cwe89_sqli.sarif.json")
BANDIT_FIXTURE = os.path.join(BASE_DIR, "tests", "fixtures", "sarif", "bandit_cwe22_path_traversal.sarif.json")
SNYK_FIXTURE = os.path.join(BASE_DIR, "tests", "fixtures", "sarif", "snyk_cwe79_xss.sarif.json")


def test_valid_sarif_parses_correctly():
    reports = parse_sarif_file(SEMGREP_FIXTURE)
    assert len(reports) == 1
    assert reports[0].cwe_id == "CWE-89"
    assert reports[0].scanner == "semgrep"
    assert reports[0].start_line == 28


def test_invalid_sarif_raises_validation_error(tmp_path):
    invalid_file = tmp_path / "bad.sarif"
    invalid_file.write_text('{"invalid": "schema"}', encoding="utf-8")
    with pytest.raises(ValueError, match="does not match valid SARIF"):
        parse_sarif_file(str(invalid_file))


def test_semgrep_adapter_normalization():
    reports = parse_sarif_file(SEMGREP_FIXTURE)
    assert len(reports) == 1
    r = reports[0]
    assert r.cwe_id == "CWE-89"
    assert r.severity in ["HIGH", "CRITICAL"]
    assert "skull" in r.skull_score
    assert r.sink_symbol == "cursor.execute(query)"


def test_snyk_adapter_normalization():
    reports = parse_sarif_file(SNYK_FIXTURE)
    assert len(reports) == 1
    r = reports[0]
    assert r.cwe_id == "CWE-79"
    assert r.scanner == "snyk"
    assert r.start_line == 22
    assert "skull" in r.skull_score


def test_bandit_adapter_normalization():
    reports = parse_sarif_file(BANDIT_FIXTURE)
    assert len(reports) == 1
    r = reports[0]
    assert r.cwe_id == "CWE-22"
    assert r.scanner == "bandit"
    assert r.start_line == 15


def test_cwe_id_extraction():
    reports_semgrep = parse_sarif_file(SEMGREP_FIXTURE)
    assert reports_semgrep[0].cwe_id.startswith("CWE-")
    
    reports_bandit = parse_sarif_file(BANDIT_FIXTURE)
    assert reports_bandit[0].cwe_id.startswith("CWE-")


def test_physical_location_mapping():
    loc_dict = {
        "physicalLocation": {
            "artifactLocation": {"uri": "backend/auth.py"},
            "region": {
                "startLine": 42,
                "endLine": 45,
                "startColumn": 5,
                "endColumn": 20,
                "snippet": {"text": "check_password(input)"}
            }
        }
    }
    loc = normalize_location(loc_dict)
    assert loc.file_path == "backend/auth.py"
    assert loc.start_line == 42
    assert loc.end_line == 45
    assert loc.start_col == 5
    assert loc.end_col == 20
    assert loc.sink_symbol == "check_password(input)"

