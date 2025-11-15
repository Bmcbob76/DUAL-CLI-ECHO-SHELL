@echo off
REM ECHO PRIME - Quick Launch Script
REM Authority Level 11.0 - Commander Bobby Don McWilliams II

echo.
echo ======================================================================
echo      ECHO PRIME AI COMMAND CENTER - LAUNCH SEQUENCE
echo ======================================================================
echo.

REM Kill any existing instances
echo [1/4] Terminating existing servers...
taskkill /F /FI "WINDOWTITLE eq Administrator:  ECHO PRIME*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM Launch Bridge Server
echo [2/4] Starting AI Bridge Server (port 8765)...
start "ECHO PRIME - Bridge Server" /MIN H:\Tools\python.exe P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\ai_bridge_server.py
timeout /t 3 /nobreak >nul

REM Launch GUI Backend
echo [3/4] Starting GUI Backend Server (port 8766)...
start "ECHO PRIME - GUI Backend" /MIN H:\Tools\python.exe P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI\gui_server.py
timeout /t 2 /nobreak >nul

REM Open in Browser
echo [4/4] Opening GUI in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8766

echo.
echo ======================================================================
echo      LAUNCH COMPLETE
echo ======================================================================
echo.
echo     Bridge API:  http://localhost:8765
echo     GUI:         http://localhost:8766
echo.
echo     Status Check: http://localhost:8765/health
echo.
echo     Press any key to view server logs...
echo ======================================================================
echo.
pause
