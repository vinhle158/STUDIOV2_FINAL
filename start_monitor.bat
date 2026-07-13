@echo off
echo ========================================================
echo STUDIO V2 - SYSTEM MONITOR SERVER
echo ========================================================
echo.
echo Dang khoi dong Local Server de doc file markdown...
start /b python -m http.server 8080 > NUL 2>&1

echo Cho 2 giay de server khoi dong...
timeout /t 2 /nobreak > NUL

echo Dang mo trinh duyet...
start http://localhost:8080/monitor.html

echo.
echo ========================================================
echo Dashboard da mo tren trinh duyet.
echo De dong server, tat cua so CMD nay.
echo ========================================================
pause
