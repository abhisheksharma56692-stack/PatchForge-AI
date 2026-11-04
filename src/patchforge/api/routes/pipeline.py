"""WebSocket endpoint for real-time state machine streaming."""
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from patchforge.orchestrator.callbacks import register_websocket, unregister_websocket

router = APIRouter(tags=["pipeline"])


@router.websocket("/ws/pipeline")
async def pipeline_websocket_endpoint(websocket: WebSocket):
    """Establishes real-time bi-directional pipeline telemetry streaming."""
    await websocket.accept()
    register_websocket(websocket)
    try:
        # Send initial connection handshake
        await websocket.send_json({
            "event": "CONNECTED",
            "message": "🎃 Connected to PatchForge AI Live Pipeline Telemetry",
        })
        while True:
            # Keep socket alive and receive client pings/messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        unregister_websocket(websocket)
    except Exception:
        unregister_websocket(websocket)

