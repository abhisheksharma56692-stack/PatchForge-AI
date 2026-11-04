"""Execution lifecycle callbacks and WebSocket event broadcasting."""
import asyncio
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("patchforge.orchestrator")

# Active WebSocket connections registered by the FastAPI server
ACTIVE_WEBSOCKETS: List[Any] = []


def register_websocket(ws: Any) -> None:
    if ws not in ACTIVE_WEBSOCKETS:
        ACTIVE_WEBSOCKETS.append(ws)


def unregister_websocket(ws: Any) -> None:
    if ws in ACTIVE_WEBSOCKETS:
        ACTIVE_WEBSOCKETS.remove(ws)


async def broadcast_event(event_type: str, data: Dict[str, Any]) -> None:
    """Broadcasts pipeline telemetry to all connected dashboard WebSocket clients."""
    payload = json.dumps({"event": event_type, "data": data})
    disconnected = []
    for ws in list(ACTIVE_WEBSOCKETS):
        try:
            await ws.send_text(payload)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        unregister_websocket(ws)


def notify_pipeline_step(step_name: str, status: str, details: Dict[str, Any]) -> None:
    """Synchronous hook called by orchestrator nodes to log and notify."""
    spooky_icons = {
        "ingest": "🕷️",
        "slice": "🔬",
        "solve": "🔮",
        "synthesize_test": "🗡️",
        "synthesize_patch": "🛡️",
        "audit": "⚖️",
        "sandbox": "🧪",
        "mutation": "🧬",
        "delta_sast": "🔍",
        "reflect": "🕯️",
        "dispatch": "⚰️",
        "escalate": "🚨",
    }
    icon = spooky_icons.get(step_name, "🎃")
    logger.info(f"{icon} [Pipeline Step: {step_name.upper()}] Status: {status}")

    # Fire background task if an asyncio event loop is running
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(broadcast_event("NODE_TRANSITION", {
            "step": step_name,
            "status": status,
            "details": details,
        }))
    except RuntimeError:
        pass
