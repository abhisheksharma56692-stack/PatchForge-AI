@echo off
title 🎃 PatchForge AI Launcher
echo =====================================================================
echo  🎃 Launching PatchForge AI (Backend API + Database + Frontend UI)
echo =====================================================================
start "🎃 PatchForge AI Backend" cmd /k "start_backend.bat"
timeout /t 3 /nobreak >nul
start "🎃 PatchForge AI Dashboard" cmd /k "start_frontend.bat"
echo.
echo Both services have been launched!
echo - Backend API:  http://127.0.0.1:8000
echo - Swagger Docs: http://127.0.0.1:8000/docs
echo - Frontend UI:  http://localhost:5173
echo.

