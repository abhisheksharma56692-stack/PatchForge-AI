"""Resource quota manager enforcing Linux cgroup constraints on sandboxes."""
from typing import Dict, Any


class CgroupQuotaManager:
    """Configures hard CPU, RAM, and PID cgroup constraints."""

    def __init__(
        self,
        memory_limit: str = "2048m",
        cpu_quota: float = 2.0,
        pids_limit: int = 100,
    ):
        self.memory_limit = memory_limit
        self.cpu_quota = cpu_quota
        self.pids_limit = pids_limit

    def get_container_cgroup_kwargs(self) -> Dict[str, Any]:
        """Returns Docker SDK keyword arguments for strict cgroups and security."""
        return {
            "mem_limit": self.memory_limit,
            "nano_cpus": int(self.cpu_quota * 1_000_000_000),
            "pids_limit": self.pids_limit,
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
            "read_only": True,
        }

