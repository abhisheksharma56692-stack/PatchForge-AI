$env:PYTHONPATH="src"
$env:PYTHONIOENCODING="utf-8"
Write-Host "🎃 [BACKEND] Starting PatchForge AI Backend Engine (FastAPI + SQLite + Z3)..." -ForegroundColor DarkYellow
Write-Host "🎃 [BACKEND] API Endpoint: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "🎃 [BACKEND] Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
python -m uvicorn patchforge.api.server:app --host 0.0.0.0 --port 8000 --reload

