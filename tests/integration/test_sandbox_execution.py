"""Integration tests for Hermetic Docker sandbox."""
import os
import pytest
from patchforge.sandbox.container_client import HermeticSandboxHarness
from patchforge.sandbox.cgroup_manager import CgroupQuotaManager
from patchforge.sandbox.network_guard import NetworkAirGapGuard, SecurityError
from patchforge.sandbox.patch_applier import PatchApplier


def test_sandbox_cgroup_and_airgap_config():
    cgroup = CgroupQuotaManager(memory_limit="2048m", cpu_quota=2.0)
    kwargs = cgroup.get_container_cgroup_kwargs()
    assert kwargs["mem_limit"] == "2048m"
    assert kwargs["nano_cpus"] == 2_000_000_000
    assert kwargs["read_only"] is True

    guard = NetworkAirGapGuard(enforced_mode="none")
    assert guard.validate_network_isolation({"network_mode": "none"}) is True

    with pytest.raises(SecurityError, match="Air-gap breach"):
        guard.validate_network_isolation({"network_mode": "bridge"})


def test_sandbox_execution_runner():
    harness = HermeticSandboxHarness()
    # Runs safe command with Windows-compatible quoting
    res = harness.execute_in_sandbox(repo_mount_dir=".", command='python -c "print(\'Sandbox ok\')"')
    assert res.exit_code == 0
    assert "Sandbox ok" in res.stdout
    assert res.reproduction_defended is True


def test_patch_applier_invalid_diff(tmp_path):
    applier = PatchApplier()
    success, msg = applier.apply_patch(str(tmp_path), "invalid diff content")
    assert not success
