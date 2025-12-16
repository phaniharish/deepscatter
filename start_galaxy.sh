#!/bin/bash
# Cleanup
pkill -f "threaded_server.py"
pkill -f "vite"

echo "---------------------------------------------------"
echo "  🌌 GALAXY LAUNCHER"
echo "---------------------------------------------------"
echo "1. Starting Image Backend (Port 8123)..."
python3 threaded_server.py > /dev/null 2>&1 &

echo "2. Starting Frontend (Port 3344)..."
echo "👉 Open http://localhost:3344/"
echo "---------------------------------------------------"

# Force prevents cache issues, Host allows external access
npm run dev -- --host --force
