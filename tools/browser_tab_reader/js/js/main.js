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

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);