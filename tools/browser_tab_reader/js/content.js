// Content script that bridges between webpage and extension
const messageHandlers = {
    GET_TABS: async () => {
        try {
            const tabs = await browser.tabs.query({});
            return { success: true, tabs };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },
    
    GET_RULES: async () => {
        try {
            const response = await fetch(browser.runtime.getURL('rules.json'));
            const rules = await response.json();
            return { success: true, rules };
        } catch (error) {
            return { 
                success: false, 
                error: error.message,
                fallbackRules: [
                    { domain: "dictionary.com", pattern: "/browse/([^/?#]+)" },
                    { domain: "merriam-webster.com", pattern: "/dictionary/([^/?#]+)" }
                ]
            };
        }
    }
};

window.addEventListener('message', async (event) => {
    if (event.source !== window || !event.data.type) return;
    
    const handler = messageHandlers[event.data.type];
    if (handler) {
        const response = await handler();
        window.postMessage({
            type: `${event.data.type}_RESPONSE`,
            ...response
        }, '*');
    }
});