# Web DOM Capture

A simple Chrome extension and Python server combination to capture the complete DOM of a webpage and save it locally.

## Architecture

This project uses a client-server model:
- **Chrome Extension (Client):** A lightweight extension that, upon clicking its icon, captures the active tab's full DOM (`outerHTML`) and its URL. It then sends this data to a local Python server.
- **Python Flask Server (Server):** A simple local server that listens for POST requests. It receives the DOM and URL, saves the content into a new HTML file in the `captured_doms` directory, and returns the absolute path of the new file along with a short usage guide.

This architecture was chosen for its simplicity and reliability (KISS principle) after an initial attempt using the File System Access API proved overly complex due to browser security restrictions.

## Features

- **One-Click Capture:** Click the extension icon to automatically capture and save the DOM.
- **Local Server:** A Flask server handles file I/O, removing the need for complex browser APIs.
- **Automatic Cleanup:** The server only keeps the latest 20 captured files, automatically deleting the oldest ones.
- **Detailed File Headers:** Each saved HTML file is prepended with a comment containing the capture timestamp, original URL, and detailed instructions on how to view the file using Linux commands.
- **Instant Feedback:** The extension popup displays the saved file path and a quick usage guide, which is also copied to the clipboard.
- **Easy Management:** Includes simple shell scripts (`start_or_restart_server.sh`, `stop_server.sh`) to manage the server process.

## How to Use

### 1. Start the Server

You need Python 3 and `pip` installed.

First, set up the virtual environment and install dependencies:
```bash
# Navigate to the server directory
cd py-server

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

Then, start the server using the management script:
```bash
# From the project root directory
./start_or_restart_server.sh
```
The server will start in the background. You can check its status in `py-server/server.log`.

To stop the server:
```bash
./stop_server.sh
```

### 2. Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions`.
2. Enable "Developer mode" (top right).
3. Click "Load unpacked".
4. Select the `web-dom-capture` project directory.
5. The extension icon will appear in your toolbar.

### 3. Capture a DOM

1. Navigate to any webpage.
2. Click the "Web DOM Capture" extension icon in your toolbar.
3. The DOM will be saved automatically, and the file path and instructions will be copied to your clipboard. The captured files are located in the `captured_doms` directory.

## Authors

- Lâm Thanh Phong (Banking University HCMC)
- NexiumLab AI

## License

This project is for internal use only.
