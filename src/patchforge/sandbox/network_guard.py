"""Air-gap verification guard enforcing zero-network container isolation."""
from typing import Dict, Any


class NetworkAirGapGuard:
    """Validates that containers execute strictly with network none."""

    def __init__(self, enforced_mode: str = "none"):
        self.enforced_mode = enforced_mode

    def validate_network_isolation(self, container_config: Dict[str, Any]) -> bool:
        """Verifies network_mode is none."""
        mode = container_config.get("network_mode", "")
        if mode != self.enforced_mode:
            raise SecurityError(
                f"Air-gap breach detected! Network mode must be '{self.enforced_mode}', got '{mode}'"
            )
        return True

    def get_airgap_kwargs(self) -> Dict[str, Any]:
        """Returns standard container creation air-gap flags."""
        return {"network_mode": self.enforced_mode}


class SecurityError(Exception):
    """Raised when an air-gap or security policy is violated."""
    pass

