// Dictionary site patterns (loaded from rules.json)
let dictionarySites = [];

// Load dictionary rules via extension messaging
async function loadDictionaryRules() {
    return new Promise((resolve) => {
        window.postMessage({ type: 'GET_RULES' }, '*');
        
        const handler = (event) => {
            if (event.source !== window || event.data.type !== 'GET_RULES_RESPONSE') return;
            
            window.removeEventListener('message', handler);
            
            if (event.data.success) {
                dictionarySites = event.data.rules;
            } else {
                console.error('Failed to load rules:', event.data.error);
                dictionarySites = event.data.fallbackRules || [
                    { domain: "dictionary.com", pattern: "/browse/([^/?#]+)" },
                    { domain: "merriam-webster.com", pattern: "/dictionary/([^/?#]+)" }
                ];
            }
            resolve();
        };
        
        window.addEventListener('message', handler);
    });
}

// Global variables
let allTabs = [];
let dictionaryTabs = [];

// Check if running in Firefox
function isFirefox() {
    return navigator.userAgent.includes('Firefox');
}

// Show status message
function showStatus(message, type) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;
    statusDiv.className = type;
    statusDiv.classList.remove('hidden');
}

// Extract search term from URL
function extractSearchTerm(url, domain) {
    const matchingSite = dictionarySites.find(site => url.includes(site.domain));
    if (!matchingSite) return null;
    
    try {
        const urlObj = new URL(url);
        const match = urlObj.pathname.match(matchingSite.pattern);
        if (match && match[1]) {
            return decodeURIComponent(match[1].replace(/\+/g, ' '));
        }
        
        // Check for query parameters
        const searchParams = urlObj.searchParams;
        for (const param of ['q', 'query', 'word', 'term', 'search']) {
            if (searchParams.has(param)) {
                return searchParams.get(param);
            }
        }
    } catch (e) {
        console.error("Error parsing URL:", e);
    }
    
    return null;
}

// Initialize the application
async function init() {
    await loadDictionaryRules();
    setupMessageHandler();
    document.getElementById('readTabsBtn').addEventListener('click', readTabs);
    document.getElementById('saveJsonBtn').addEventListener('click', saveJson);
    document.getElementById('copyJsonBtn').addEventListener('click', copyJson);
}

// Message handler for extension responses
function setupMessageHandler() {
    window.addEventListener('message', (event) => {
        if (event.source !== window) return;
        
        if (event.data.type === 'GET_TABS_RESPONSE') {
            if (event.data.success) {
                allTabs = event.data.tabs;
                dictionaryTabs = allTabs
                    .filter(tab => dictionarySites.some(site => tab.url.includes(site.domain)))
                    .map(tab => ({
                        ...tab,
                        searchTerm: extractSearchTerm(tab.url, tab.url.match(/:\/\/(.[^/]+)/)[1])
                    }));
                updateResultsTable();
                showStatus(`Found ${dictionaryTabs.length} dictionary tabs`, 'success');
            } else {
                showStatus(`Failed to read tabs: ${event.data.error}`, 'error');
            }
        }
    });
}

// Read and process browser tabs
function readTabs() {
    if (!isFirefox()) {
        showStatus('This tool only works in Firefox', 'error');
        return;
    }

    showStatus('Reading tabs...', 'info');
    window.postMessage({ type: 'GET_TABS' }, '*');
    document.getElementById('saveJsonBtn').disabled = true;
    document.getElementById('copyJsonBtn').disabled = true;
}

// Update the results table with found dictionary tabs
function updateResultsTable() {
    const tableBody = document.getElementById('tabsTableBody');
    tableBody.innerHTML = '';
    
    dictionaryTabs.forEach((tab, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${tab.title}</td>
            <td><a href="${tab.url}" target="_blank">${tab.url}</a></td>
            <td>${new URL(tab.url).hostname}</td>
            <td>${tab.searchTerm || '-'}</td>
        `;
        tableBody.appendChild(row);
    });
    
    document.getElementById('dictTabCount').textContent = dictionaryTabs.length;
    document.getElementById('totalTabCount').textContent = allTabs.length;
    document.getElementById('resultsContainer').classList.remove('hidden');
}

// Save dictionary tabs as JSON file
function saveJson() {
    const jsonStr = JSON.stringify(dictionaryTabs, null, 2);
    const blob = new Blob([jsonStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dictionary_tabs.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showStatus('JSON file saved', 'success');
}

// Copy JSON to clipboard
function copyJson() {
    const jsonStr = JSON.stringify(dictionaryTabs, null, 2);
    navigator.clipboard.writeText(jsonStr)
        .then(() => showStatus('JSON copied to clipboard', 'success'))
        .catch(err => {
            console.error('Failed to copy:', err);
            showStatus('Failed to copy JSON', 'error');
        });
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);