/**
 * Sends the DOM content and URL to the local server.
 * @param {string} domContent - The HTML content of the DOM.
 * @param {string} tabUrl - The URL of the captured tab.
 * @returns {Promise<object>} - A promise that resolves to the server's JSON response.
 */
export async function sendDomToServer(domContent, tabUrl) {
  const response = await fetch('http://127.0.0.1:51234/save-dom', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ dom: domContent, url: tabUrl }),
  });

  if (!response.ok) {
    throw new Error(`Server responded with ${response.status}`);
  }

  const data = await response.json();

  if (data.status !== 'success') {
    throw new Error(data.message || 'Unknown server error.');
  }

  return data;
} 