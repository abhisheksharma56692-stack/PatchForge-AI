"""Integration tests for FastAPI dashboard backend routes."""
import pytest
from fastapi.testclient import TestClient
from patchforge.api.server import create_app

client = TestClient(create_app())


def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "Halloween" in data["theme"]


def test_api_dashboard_summary():
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "open_skulls" in data
    assert "remediated_ghosts" in data
    assert data["pipeline_health_percent"] > 90


def test_api_vulnerabilities_crypt():
    res = client.get("/api/vulns")
    assert res.status_code == 200
    vulns = res.json()
    assert len(vulns) > 0
    assert "skull_rating" in vulns[0]
    assert "cwe_id" in vulns[0]


def test_api_runs_and_graveyard():
    res = client.get("/api/runs")
    assert res.status_code == 200
    runs = res.json()
    assert len(runs) > 0

    res_grave = client.get("/api/runs/graveyard")
    assert res_grave.status_code == 200
    tombstones = res_grave.json()
    assert len(tombstones) > 0
    assert "R.I.P." in tombstones[0]["tombstone_inscription"]


def test_websocket_pipeline_connection():
    with client.websocket_connect("/ws/pipeline") as websocket:
        data = websocket.receive_json()
        assert data["event"] == "CONNECTED"
        websocket.send_text("ping")
        resp = websocket.receive_text()
        assert resp == "pong"

