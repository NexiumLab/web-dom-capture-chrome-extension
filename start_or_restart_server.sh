#!/bin/bash

# Get the absolute path of the directory where the script is located
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Change the current working directory to the script's directory
cd "$SCRIPT_DIR"

# --- Configuration ---
PORT=51234
VENV_ACTIVATE="py-server/.venv/bin/activate"
SERVER_SCRIPT="py-server/main.py"
OUTPUT_LOG="py-server/server_output.log"

echo "--- DOM Grabber Server Manager ---"

# Find the Process ID (PID) using the specified port
PID=$(lsof -t -i:$PORT)

# Check if a PID was found
if [ -n "$PID" ]; then
    echo "Server is currently running with PID: $PID. Restarting..."
    kill $PID
    # Wait a moment for the port to become free
    sleep 1
else
    echo "Server is not running. Starting..."
fi

# Activate the virtual environment and start the Python server in the background
echo "Activating virtual environment and starting server..."
source $VENV_ACTIVATE

# Use nohup to run the server in the background and redirect output to a log file
nohup python3 -u $SERVER_SCRIPT > $OUTPUT_LOG 2>&1 &

echo "✅ Server started successfully."
echo "Logs are being written to: $OUTPUT_LOG"
echo "To see live logs, run: tail -f $OUTPUT_LOG"
echo "To stop the server, run: kill \$(lsof -t -i:$PORT)" 