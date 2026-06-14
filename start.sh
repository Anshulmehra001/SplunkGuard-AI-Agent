#!/bin/bash

# SplunkGuard AI Agent - Quick Start Script (Mac/Linux)

echo "╔═══════════════════════════════════════════════════════╗"
echo "║      SplunkGuard AI Agent - Quick Start (Mac/Linux)   ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}[ERROR] backend/.env file not found!${NC}"
    echo ""
    echo "Please follow these steps:"
    echo "1. Copy backend/.env.example to backend/.env"
    echo "   $ cp backend/.env.example backend/.env"
    echo "2. Edit backend/.env and add your OpenAI API key"
    echo ""
    echo "Get API key from: https://platform.openai.com/"
    echo ""
    exit 1
fi

echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 not found! Install from https://python.org${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Python found${NC}"

echo ""
echo "[2/4] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR] Node.js not found! Install from https://nodejs.org${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Node.js found${NC}"

echo ""
echo "[3/4] Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install Python dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Backend dependencies installed${NC}"
cd ..

echo ""
echo "[4/4] Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "This may take a few minutes..."
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to install Node dependencies${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[OK] Frontend dependencies installed${NC}"
cd ..

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                 Setup Complete! 🎉                    ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Starting servers..."
echo ""
echo "Backend will start on: http://localhost:5000"
echo "Frontend will start on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start backend
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ Both servers started!${NC}"
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
