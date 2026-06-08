@echo off
color 0A
echo ====================================================
echo         STARTING UNIFIED WHATSAPP AI AGENT
echo ====================================================
echo.

echo [1/3] Launching LLM Brain Server (main.py)...
start "AI Brain (LLMs)" cmd /k "cd desktop-voice-agent && python main.py"

timeout /t 3 /nobreak >nul

echo [2/3] Launching WhatsApp Text Agent (VPS Module)...
start "Text Messaging Agent" cmd /k "cd text-agent-vps && python main.py"

timeout /t 5 /nobreak >nul

echo [3/3] Launching Desktop Voice Agent...
start "Voice Call Agent" cmd /k "cd desktop-voice-agent && python desktop_agent.py"

echo.
echo ====================================================
echo   All systems online! Agent is running in background.
echo   You can now minimize these windows.
echo ====================================================
echo.
pause
