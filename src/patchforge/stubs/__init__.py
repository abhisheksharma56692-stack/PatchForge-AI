"""Stubs package for independent integration testing."""
from patchforge.stubs.mock_sarif_parser import parse_sarif_file
from patchforge.stubs.mock_slicer import BackwardTaintSlicer
from patchforge.stubs.mock_z3_engine import SMTInvariantVerifier
from patchforge.stubs.mock_agents import (
    TestSynthesizerAgent,
    PatchSynthesizerAgent,
    AntiTamperAuditor,
    ReflectionEngine,
)

__all__ = [
    "parse_sarif_file",
    "BackwardTaintSlicer",
    "SMTInvariantVerifier",
    "TestSynthesizerAgent",
    "PatchSynthesizerAgent",
    "AntiTamperAuditor",
    "ReflectionEngine",
]

