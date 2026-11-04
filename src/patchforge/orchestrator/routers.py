"""Conditional routers for LangGraph state machine branching."""
from patchforge.models.state import RemediationGraphState


def audit_router(state: RemediationGraphState) -> str:
    """Routes based on Agent Gamma's anti-tamper audit result."""
    if state.get("audit_passed", False):
        return "sandbox"
    return "reflect"


def sandbox_router(state: RemediationGraphState) -> str:
    """Routes based on container sandbox test and defense outcome."""
    sandbox_res = state.get("sandbox_result")
    if not sandbox_res:
        return "reflect"
    
    # Dual-condition evaluation gate: Baseline tests pass AND PoC is defended/blocked
    if sandbox_res.baseline_passed and sandbox_res.reproduction_defended:
        return "mutation"
    return "reflect"


def mutation_router(state: RemediationGraphState) -> str:
    """Routes based on mutation testing threshold (>= 85%)."""
    sandbox_res = state.get("sandbox_result")
    if sandbox_res and sandbox_res.mutation_score >= 85.0:
        return "delta_sast"
    return "reflect"


def delta_sast_router(state: RemediationGraphState) -> str:
    """Routes based on Delta-SAST scan (original flaw eliminated and 0 new flaws)."""
    sandbox_res = state.get("sandbox_result")
    if sandbox_res and sandbox_res.delta_sast_clean:
        return "dispatch"
    return "reflect"


def loop_bound_router(state: RemediationGraphState) -> str:
    """Guards against infinite loops: if iteration >= max_iterations, escalate to human."""
    iteration = state.get("iteration_count", 0)
    max_k = state.get("max_iterations", 5)
    if iteration >= max_k:
        return "escalate"
    return "synthesize_patch"

