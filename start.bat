@echo off
echo ╔═══════════════════════════════════════════════════════╗
echo ║     SplunkGuard AI Agent - Quick Start (Windows)      ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo [ERROR] backend\.env file not found!
    echo.
    echo Please follow these steps:
    echo 1. Copy backend\.env.example to backend\.env
    echo 2. Edit backend\.env and add your OpenAI API key
    echo.
    echo Get API key from: https://platform.openai.com/
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Install from https://python.org
    pause
    exit /b 1
)
echo [OK] Python found

echo.
echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Install from https://nodejs.org
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo [3/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Backend dependencies installed

echo.
echo [4/4] Installing frontend dependencies...
cd ..\frontend
if not exist "node_modules" (
    echo This may take a few minutes...
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install Node dependencies
        pause
        exit /b 1
    )
)
echo [OK] Frontend dependencies installed

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║                 Setup Complete! 🎉                    ║
echo ╚═══════════════════════════════════════════════════════╝
echo.
echo Starting servers...
echo.
echo Backend will start on: http://localhost:5000
echo Frontend will start on: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend in new window
start "SplunkGuard Backend" cmd /k "cd backend && python app.py"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "SplunkGuard Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both servers started!
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo The frontend will open automatically in your browser.
echo.
pause
