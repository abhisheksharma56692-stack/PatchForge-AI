@echo off
title 🎃 PatchForge AI - Backend API & WebSocket Engine
set PYTHONPATH=src
set PYTHONIOENCODING=utf-8
echo =====================================================================
echo  🎃 Starting PatchForge AI Backend Engine (FastAPI + SQLite + Z3)
echo  Listening on: http://127.0.0.1:8000
echo  Interactive Swagger Docs: http://127.0.0.1:8000/docs
echo =====================================================================
python -m uvicorn patchforge.api.server:app --host 0.0.0.0 --port 8000 --reload
pause

