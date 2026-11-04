"""SARIF Ingestion & Parsing Subsystem."""
from patchforge.ingestion.sarif_parser import (
    parse_sarif_file,
    validate_sarif_schema,
    extract_findings,
    normalize_location,
)
from patchforge.ingestion.scanner_adapters.semgrep import SemgrepAdapter
from patchforge.ingestion.scanner_adapters.snyk import SnykAdapter
from patchforge.ingestion.scanner_adapters.bandit import BanditAdapter

__all__ = [
    "parse_sarif_file",
    "validate_sarif_schema",
    "extract_findings",
    "normalize_location",
    "SemgrepAdapter",
    "SnykAdapter",
    "BanditAdapter",
]

