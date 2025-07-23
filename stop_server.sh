#!/bin/bash
# stop_server.sh
# This script stops the Flask server for the DOM capture project.

# --- Configuration ---
# Get the port from config.py using grep and sed
CONFIG_FILE="py-server/config.py"
PORT=$(grep -oP 'PORT\s*=\s*\K[0-9]+' "$CONFIG_FILE")

if [ -z "$PORT" ]; then
    echo "Error: Could not find PORT in $CONFIG_FILE"
    exit 1
fi

echo "--- Stopping DOM Capture Server ---"
echo "Port: $PORT"

# Find the PID of the process using the specified port
PID=$(lsof -t -i:$PORT)

if [ -z "$PID" ]; then
    echo "Server is not running on port $PORT."
else
    echo "Found server process with PID: $PID"
    kill "$PID"
    echo "Server stopped successfully."
fi 