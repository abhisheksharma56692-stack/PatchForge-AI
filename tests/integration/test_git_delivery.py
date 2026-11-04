"""Integration tests for Git delivery operations."""
import os
import pytest
from patchforge.delivery.git_manager import GitRemediationManager
from patchforge.delivery.github_client import GitHubDeliveryClient


def test_git_branch_naming():
    manager = GitRemediationManager(repo_path=".")
    branch = manager.create_remediation_branch("CWE-89")
    assert "patchforge/remediate-cwe89-" in branch


def test_github_pr_mock_dispatch():
    client = GitHubDeliveryClient(token=None)
    pr_url = client.create_pull_request(
        repo_name="org/repo",
        head_branch="patchforge/remediate-cwe89-1234",
        title="Remediate CWE-89",
        body="PR Body",
    )
    assert "github.com/org/repo/pull/" in pr_url

