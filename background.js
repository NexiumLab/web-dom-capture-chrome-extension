// --- IndexedDB Helper (KISS version) ---
const idb = {
  db: null,
  async init() {
    if (this.db) return;
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('DOMGrabberDB', 4); // Version 4
      request.onupgradeneeded = e => e.target.result.createObjectStore('keyval');
      request.onerror = e => reject('DB Error');
      request.onsuccess = e => { this.db = e.target.result; resolve(); };
    });
  },
  async get(key) { await this.init(); return new Promise(r => this.db.transaction('keyval').objectStore('keyval').get(key).onsuccess = e => r(e.target.result)); },
  async set(key, value) { await this.init(); return new Promise(r => this.db.transaction('keyval', 'readwrite').objectStore('keyval').put(value, key).onsuccess = e => r()); }
};

async function sendDomToServer(domContent) {
  const url = 'http://127.0.0.1:51234/save-dom';
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dom: domContent }),
    });
    // Trả về toàn bộ response JSON từ server
    const responseData = await response.json();
    console.log("Received from server:", responseData);
    return responseData;
  } catch (error) {
    console.error('Error sending DOM to server:', error);
    // Trả về một object lỗi để popup có thể xử lý
    return { status: "error", message: `Không thể kết nối tới server: ${error.message}` };
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'grabDOM') {
    // Wrap the logic in an async IIFE
    (async () => {
      try {
        const injectionResults = await chrome.scripting.executeScript({
          target: { tabId: request.tabId }, // Use tabId from the message
          func: () => document.documentElement.outerHTML,
        });

        if (injectionResults && injectionResults[0] && injectionResults[0].result) {
          const serverResponse = await sendDomToServer(injectionResults[0].result);
          sendResponse(serverResponse);
        } else {
          sendResponse({ status: "error", message: "Không thể lấy DOM từ trang." });
        }
      } catch (e) {
        console.error("Lỗi trong quá trình lấy DOM:", e);
        sendResponse({ status: "error", message: `Lỗi script: ${e.message}` });
      }
    })();

    return true; // This is critical. It tells Chrome to keep the message port open for an async response.
  }
}); 