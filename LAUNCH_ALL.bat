@echo off
REM ECHO PRIME - Complete System Launcher
REM Starts CLI Bridge + GUI Server

echo ========================================
echo ECHO PRIME - UNIFIED AI COMMAND CENTER
echo ========================================
echo.

cd /d P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION

echo [1/3] Starting CLI Bridge Server...
start "CLI Bridge" H:\Tools\python.exe ai_bridge_server.py

timeout /t 3 /nobreak >nul

echo [2/3] Starting GUI Backend Server...
cd GUI
start "GUI Backend" H:\Tools\python.exe gui_server.py

timeout /t 3 /nobreak >nul

echo [3/3] Opening Web GUI...
start http://localhost:8766

echo.
echo ========================================
echo SYSTEM OPERATIONAL
echo ========================================
echo.
echo CLI Bridge:  http://localhost:8765
echo GUI Backend: http://localhost:8766
echo Web GUI:     http://localhost:8766 (opened in browser)
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq CLI Bridge*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq GUI Backend*" /T /F >nul 2>&1

echo.
echo Servers stopped.
pause
