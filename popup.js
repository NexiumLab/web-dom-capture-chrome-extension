// popup.js

import { sendDomToServer } from './js/api.js';

document.addEventListener('DOMContentLoaded', function() {
  const statusDiv = document.getElementById('status');
  const logTextarea = document.getElementById('log');
  const loadingGif = document.getElementById('loading-gif');

  statusDiv.textContent = 'Capturing DOM...';
  logTextarea.value = '';
  loadingGif.classList.remove('hidden'); // Show loading GIF

  // 1. Get the current active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentTab = tabs[0];
    if (!currentTab) {
      statusDiv.textContent = 'Error: No active tab found.';
      return;
    }

    const tabId = currentTab.id;
    const tabUrl = currentTab.url;

    // 2. Execute script in the tab to get its DOM
    chrome.scripting.executeScript(
      {
        target: { tabId: tabId },
        func: () => document.documentElement.outerHTML,
      },
      (injectionResults) => {
        if (chrome.runtime.lastError || !injectionResults || !injectionResults[0]) {
          statusDiv.textContent = 'Error: Failed to capture DOM.';
          logTextarea.value = chrome.runtime.lastError ? chrome.runtime.lastError.message : 'No result from script injection.';
          loadingGif.classList.add('hidden'); // Hide loading GIF on error
          return;
        }

        const domContent = injectionResults[0].result;
        statusDiv.textContent = 'DOM captured. Sending to server...';

        // 3. Send the DOM to the local Python server
        sendDomToServer(domContent, tabUrl)
          .then(data => {
            // Add a 1-second delay to show the animation
            setTimeout(() => {
              loadingGif.classList.add('hidden'); // Hide loading GIF on success
              statusDiv.textContent = 'Success! DOM saved.';
              
              const logMessage = `DOM saved to file. File Path: ${data.file_path}\n\n--- View Instructions ---\n${data.guide}`;
              logTextarea.value = logMessage;
  
              // 4. Copy the log message to clipboard
              navigator.clipboard.writeText(logMessage).then(() => {
                statusDiv.textContent = '✅ Success! Log copied to clipboard.';
              }).catch(err => {
                statusDiv.textContent = 'Success! (Clipboard copy failed).';
                console.error('Failed to copy to clipboard:', err);
              });
            }, 1000); // 1-second fake delay
          })
          .catch(error => {
            loadingGif.classList.add('hidden'); // Hide loading GIF on error
            statusDiv.textContent = 'Error: Could not send to server.';
            logTextarea.value = `Failed to send DOM to server.\nError: ${error.message}\n\nPlease ensure the Python server is running.`;
            console.error('Fetch error:', error);
          });
      }
    );
  });
}); 