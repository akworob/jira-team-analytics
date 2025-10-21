@echo off
echo ============================
echo JIRA Dashboard Installer
echo ============================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python nie jest zainstalowany!
    echo Zainstaluj Python 3.7+ i dodaj do PATH.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo OK: Python znaleziony
python --version
echo.

REM Create virtual environment
echo Tworzenie srodowiska wirtualnego...
python -m venv venv

REM Activate virtual environment
echo Aktywacja srodowiska...
call venv\Scripts\activate.bat

REM Install requirements
echo Instalacja zaleznosci...
pip install -r requirements.txt

echo.
echo ============================
echo Instalacja zakonczona!
echo ============================
echo.
echo Aby uruchomic dashboard:
echo 1. Aktywuj srodowisko: venv\Scripts\activate
echo 2. Uruchom serwer: python jira_proxy_server.py
echo 3. Otworz przegladarke: http://localhost:5000
echo 4. Lub otworz bezposrednio: jira_dashboard.html
echo.
echo Milej pracy!
pause
