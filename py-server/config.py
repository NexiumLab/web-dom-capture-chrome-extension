# === Server Configuration for DOM Grabber ===

# --- Network Settings ---
PORT = 51234

# --- Directory and File Limits ---
# Absolute path to the directory where DOM files will be saved.
# The server will navigate up one level from its own directory ('py-server')
# and then into 'captured_doms'.
import os
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIRECTORY = os.path.join(SERVER_DIR, '..', 'captured_doms')

# Maximum number of files to keep in the SAVE_DIRECTORY.
# When this limit is exceeded, the oldest files will be deleted.
MAX_FILES =  1000
# --- Logging ---
LOG_FILE = os.path.join(SERVER_DIR, 'server.log')

# --- Instructions for Client ---
LINUX_COMMAND_GUIDE = """Quick guide for inspecting the captured DOM file:
- [RECOMMENDED] Hoặc dùng MCP "fong-long-file-reader" để đọc file dài
- Check file size: `wc -l "{file_path}"`
- For small files (<200 LOC), use `cat`. For larger files, use `less`, `sed` or `grep`.
- For full instructions, view the first 100 lines of this file: `head -n 100 "{file_path}"`"""



SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'captured_doms')

VIEW_FILE_INSTRUCTIONS = """
This guide provides common Linux commands to inspect and read the captured DOM HTML file.

Commands below: {file_path}
---------------------------------------------------------------------
0.  [RECOMMENDED] Use MCP for Large Files
---------------------------------------------------------------------
    # If you have access to MCP "fong-long-file-reader", use it for large files
    # This provides better analysis and reading experience for files >200 lines
    # Simply mention the file path to your AI assistant with MCP access

---------------------------------------------------------------------
1.  Check File Size & Basic Info
---------------------------------------------------------------------
    # Get line, word, and character count
    wc -l {file_path}

---------------------------------------------------------------------
2.  View the Beginning or End of the File
---------------------------------------------------------------------
    # View the first 40 lines (to see metadata comment)
    head -n 40 {file_path}

    # View the last 20 lines
    tail -n 20 {file_path}

---------------------------------------------------------------------
3.  View File Content Page by Page
---------------------------------------------------------------------
    # View content using 'less' (recommended, allows scrolling up/down)
    # Use arrow keys to navigate, '/' to search, 'q' to quit.
    less {file_path}

---------------------------------------------------------------------
4.  Extract Specific HTML Elements (grep)
---------------------------------------------------------------------
    # Find the <title> tag
    grep -i '<title>' {file_path}

    # Find all <h1> tags (case-insensitive)
    grep -i '<h1>' {file_path}

    # Find elements with a specific id (e.g., id="main-content")
    grep -i 'id="main-content"' {file_path}

    # Show line numbers for matches
    grep -n '<body>' {file_path}

    # Show 5 lines of context around <body> tag
    grep -C 5 '<body>' {file_path}
---------------------------------------------------------------------
5.  View Formatted HTML in Terminal (Advanced)
---------------------------------------------------------------------
    # Use w3m to render the HTML file in the terminal
    w3m {file_path}
""" 