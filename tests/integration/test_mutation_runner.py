"""Integration tests for mutation testing runner."""
import pytest
from patchforge.sandbox.mutation_runner import MutationTestRunner
from patchforge.sandbox.delta_sast import DeltaSASTScanner


def test_mutation_runner_threshold():
    runner = MutationTestRunner(threshold=85.0)
    report = runner.run_mutation_suite(repo_dir=".")
    assert report.total_mutants > 0
    assert report.mutation_score >= 85.0
    assert report.passed_threshold is True


def test_delta_sast_clean_scan():
    scanner = DeltaSASTScanner()
    report = scanner.scan_after_patch(repo_dir=".", target_rule="CWE-89")
    assert report.clean is True
    assert report.original_finding_cleared is True
    assert report.new_findings_count == 0

