#!/bin/bash

# JIRA Dashboard Startup Script
# This script starts the local server and opens the dashboard in your browser

echo "🚀 Starting JIRA Dashboard..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Start the server
echo "📡 Starting server on http://localhost:8000"
python3 server.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Open browser
echo "🌐 Opening dashboard in browser..."
open "http://localhost:8000/jira_dashboard.html"

echo ""
echo "✅ Dashboard is running!"
echo "📊 URL: http://localhost:8000/jira_dashboard.html"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for Ctrl+C
wait $SERVER_PID
