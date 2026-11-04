"""LangGraph State Graph definition for PatchForge autonomous remediation."""
from typing import Dict, Any, Callable
from patchforge.models.state import RemediationGraphState
from patchforge.orchestrator.nodes import (
    ingest_node,
    slice_node,
    solve_node,
    synthesize_test_node,
    synthesize_patch_node,
    audit_node,
    sandbox_node,
    mutation_node,
    delta_sast_node,
    reflect_node,
    dispatch_node,
    escalate_node,
)
from patchforge.orchestrator.routers import (
    audit_router,
    sandbox_router,
    mutation_router,
    delta_sast_router,
    loop_bound_router,
)


class RemediationPipelineGraph:
    """
    Executes the multi-stage adversarial remediation loop as a stateful graph.
    Compatible with LangGraph StateGraph API.
    """

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the pipeline state machine until reaching a terminal state."""
        current_state = dict(state)

        # 1. Ingest
        up = ingest_node(current_state)
        current_state.update(up)

        # 2. Slice
        up = slice_node(current_state)
        current_state.update(up)

        # 3. Solve Invariants
        up = solve_node(current_state)
        current_state.update(up)

        # 4. Synthesize Security Test (Agent Alpha)
        up = synthesize_test_node(current_state)
        current_state.update(up)

        # Iterative Closed Loop
        while True:
            # 5. Synthesize Patch (Agent Beta)
            up = synthesize_patch_node(current_state)
            current_state.update(up)

            # 6. Audit Patch (Agent Gamma)
            up = audit_node(current_state)
            current_state.update(up)

            if audit_router(current_state) == "reflect":
                up = reflect_node(current_state)
                current_state.update(up)
                if loop_bound_router(current_state) == "escalate":
                    up = escalate_node(current_state)
                    current_state.update(up)
                    return current_state
                continue

            # 7. Sandbox Execution
            up = sandbox_node(current_state)
            current_state.update(up)

            if sandbox_router(current_state) == "reflect":
                up = reflect_node(current_state)
                current_state.update(up)
                if loop_bound_router(current_state) == "escalate":
                    up = escalate_node(current_state)
                    current_state.update(up)
                    return current_state
                continue

            # 8. Mutation Verification
            up = mutation_node(current_state)
            current_state.update(up)

            if mutation_router(current_state) == "reflect":
                up = reflect_node(current_state)
                current_state.update(up)
                if loop_bound_router(current_state) == "escalate":
                    up = escalate_node(current_state)
                    current_state.update(up)
                    return current_state
                continue

            # 9. Delta-SAST Scan
            up = delta_sast_node(current_state)
            current_state.update(up)

            if delta_sast_router(current_state) == "reflect":
                up = reflect_node(current_state)
                current_state.update(up)
                if loop_bound_router(current_state) == "escalate":
                    up = escalate_node(current_state)
                    current_state.update(up)
                    return current_state
                continue

            # 10. Success -> Dispatch
            up = dispatch_node(current_state)
            current_state.update(up)
            return current_state


def build_remediation_graph():
    """Builds and returns the compiled state graph engine."""
    try:
        from langgraph.graph import StateGraph, END
        workflow = StateGraph(RemediationGraphState)
        
        # Add nodes
        workflow.add_node("ingest", ingest_node)
        workflow.add_node("slice", slice_node)
        workflow.add_node("solve", solve_node)
        workflow.add_node("synthesize_test", synthesize_test_node)
        workflow.add_node("synthesize_patch", synthesize_patch_node)
        workflow.add_node("audit", audit_node)
        workflow.add_node("sandbox", sandbox_node)
        workflow.add_node("mutation", mutation_node)
        workflow.add_node("delta_sast", delta_sast_node)
        workflow.add_node("reflect", reflect_node)
        workflow.add_node("dispatch", dispatch_node)
        workflow.add_node("escalate", escalate_node)

        # Set entry point
        workflow.set_entry_point("ingest")

        # Linear edges
        workflow.add_edge("ingest", "slice")
        workflow.add_edge("slice", "solve")
        workflow.add_edge("solve", "synthesize_test")
        workflow.add_edge("synthesize_test", "synthesize_patch")
        workflow.add_edge("synthesize_patch", "audit")

        # Conditional edges
        workflow.add_conditional_edges("audit", audit_router, {"sandbox": "sandbox", "reflect": "reflect"})
        workflow.add_conditional_edges("sandbox", sandbox_router, {"mutation": "mutation", "reflect": "reflect"})
        workflow.add_conditional_edges("mutation", mutation_router, {"delta_sast": "delta_sast", "reflect": "reflect"})
        workflow.add_conditional_edges("delta_sast", delta_sast_router, {"dispatch": "dispatch", "reflect": "reflect"})
        workflow.add_conditional_edges("reflect", loop_bound_router, {"synthesize_patch": "synthesize_patch", "escalate": "escalate"})

        workflow.add_edge("dispatch", END)
        workflow.add_edge("escalate", END)

        return workflow.compile()
    except Exception:
        return RemediationPipelineGraph()

