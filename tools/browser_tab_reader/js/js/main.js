// Dictionary site patterns
const dictionarySites = [
    { domain: "dictionary.com", pattern: /\/browse\/([^\/\?#]+)/ },
    { domain: "merriam-webster.com", pattern: /\/dictionary\/([^\/\?#]+)/ },
    { domain: "vocabulary.com", pattern: /\/dictionary\/([^\/\?#]+)/ },
    { domain: "thefreedictionary.com", pattern: /\/([^\/\?#]+)$/ },
    { domain: "dictionary.cambridge.org", pattern: /\/dictionary\/[^\/]+\/([^\/\?#]+)/ },
    { domain: "oxforddictionaries.com", pattern: /\/definition\/([^\/\?#]+)/ },
    { domain: "collinsdictionary.com", pattern: /\/dictionary\/[^\/]+\/([^\/\?#]+)/ },
    { domain: "macmillandictionary.com", pattern: /\/dictionary\/[^\/]+\/([^\/\?#]+)/ },
    { domain: "ldoceonline.com", pattern: /\/dictionary\/[^\/]+\/([^\/\?#]+)/ },
    { domain: "lexico.com", pattern: /\/definition\/([^\/\?#]+)/ },
    { domain: "etymonline.com", pattern: /\/word\/([^\/\?#]+)/ },
    { domain: "wordreference.com", pattern: /\/([^\/\?#]+)$/ },
    { domain: "urbandictionary.com", pattern: /\/define\.php\?term=([^&]+)/ },
    { domain: "wiktionary.org", pattern: /\/wiki\/([^:]+)$/ },
    { domain: "thesaurus.com", pattern: /\/browse\/([^\/\?#]+)/ }
];

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
function init() {
    document.getElementById('readTabsBtn').addEventListener('click', readTabs);
    document.getElementById('saveJsonBtn').addEventListener('click', saveJson);
    document.getElementById('copyJsonBtn').addEventListener('click', copyJson);
}

// Read and process browser tabs
function readTabs() {
    if (!isFirefox()) {
        showStatus('This tool only works in Firefox', 'error');
        return;
    }

    showStatus('Reading tabs...', 'info');
    
    browser.tabs.query({})
        .then(tabs => {
            allTabs = tabs;
            dictionaryTabs = tabs
                .filter(tab => dictionarySites.some(site => tab.url.includes(site.domain)))
                .map(tab => ({
                    ...tab,
                    searchTerm: extractSearchTerm(tab.url, tab.url.match(/:\/\/(.[^/]+)/)[1])
                }));
            
            updateResultsTable();
            document.getElementById('saveJsonBtn').disabled = false;
            document.getElementById('copyJsonBtn').disabled = false;
            showStatus(`Found ${dictionaryTabs.length} dictionary tabs`, 'success');
        })
        .catch(err => {
            console.error('Error reading tabs:', err);
            showStatus('Failed to read tabs. Make sure you have tabs permission.', 'error');
            document.getElementById('permissionsGuide').classList.remove('hidden');
        });
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