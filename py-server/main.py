import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import config
from logging.handlers import RotatingFileHandler

# --- Logging Setup ---
# Use LOG_FILE from config, default to 'server.log'
log_file = getattr(config, 'LOG_FILE', 'server.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# --- Flask App ---
app = Flask(__name__)

# -- Constants from Config --
PORT = config.PORT
SAVE_DIR = config.SAVE_DIR
MAX_FILES = config.MAX_FILES
VIEW_FILE_INSTRUCTIONS = config.VIEW_FILE_INSTRUCTIONS

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def manage_captured_files():
    """
    Manages the number of captured files by deleting the oldest ones if the count exceeds MAX_FILES.
    """
    try:
        files = [os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR)]
        files.sort(key=os.path.getctime) # Sort by creation time (oldest first)

        if len(files) > MAX_FILES:
            files_to_delete = files[:len(files) - MAX_FILES]
            logging.info(f"File limit ({MAX_FILES}) exceeded. Deleting {len(files_to_delete)} oldest files.")
            for f_path in files_to_delete:
                os.remove(f_path)
                logging.info(f"Deleted: {os.path.basename(f_path)}")
    except Exception as e:
        logging.error(f"Error during directory cleanup: {e}", exc_info=True)


def save_dom_to_file(dom_content, url):
    """Saves the given DOM content to a file with a timestamp and returns the full path."""
    now = datetime.now()
    file_name = f"dom_{now.strftime('%Y-%m-%d_%H-%M-%S-%f')}.html"
    # Use os.path.abspath to resolve the '..' and create a clean, absolute path
    file_path = os.path.abspath(os.path.join(SAVE_DIR, file_name))
    
    # --- Instructions Header ---
    # Use the DETAILED instructions for the file header
    instructions = config.VIEW_FILE_INSTRUCTIONS.format(file_path=file_path)
    header_comment = f"""<!--
Capture Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')}
Captured URL: {url}

{instructions}
-->
"""
    
    full_content = header_comment + "\n" + dom_content

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        logging.info(f"Success! DOM saved to {file_name}")
        return file_path
    except IOError as e:
        logging.error(f"Error saving file {file_name}: {e}")
        return None

@app.route('/save-dom', methods=['POST'])
def save_dom():
    """Flask route to receive and save the DOM."""
    logging.info("Received request for /save-dom")
    
    # Get data from POST request
    data = request.get_json()
    if not data or 'dom' not in data:
        logging.warning("Received invalid data.")
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    
    dom_content = data['dom']
    url = data.get('url', 'N/A')

    # Save DOM content to a new file
    file_path = save_dom_to_file(dom_content, url)
    
    if file_path:
        # Clean up old files after a successful save
        manage_captured_files()
        
        # Use the SHORT guide for the JSON response (for popup and clipboard)
        guide = config.LINUX_COMMAND_GUIDE.format(file_path=file_path)

        return jsonify({
            "status": "success",
            "message": "DOM saved successfully.",
            "file_path": file_path,
            "guide": guide
        })
    else:
        return jsonify({"status": "error", "message": "Failed to save DOM"}), 500

if __name__ == '__main__':
    logging.info(f"--- DOM Capture Server starting ---")
    logging.info(f"Listening on http://127.0.0.1:{PORT}")
    logging.info(f"Saving files to: {os.path.abspath(SAVE_DIR)}")
    logging.info(f"Max files limit set to: {MAX_FILES}")
    app.run(host='127.0.0.1', port=PORT, debug=False) 