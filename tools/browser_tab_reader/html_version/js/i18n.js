// Internationalization strings
const i18nStrings = {
    "app_title": {
        "en": "Firefox Tab Reader",
        "zh": "Firefox 标签页阅读器"
    },
    "app_subtitle": {
        "en": "Browser Tab Dictionary Tool",
        "zh": "浏览器标签页词典工具"
    },
    "instructions_title": {
        "en": "Instructions",
        "zh": "使用说明"
    },
    "instructions_content": {
        "en": "This tool extracts all your open Firefox tabs and identifies dictionary websites...",
        "zh": "此工具提取您所有打开的Firefox标签页并识别词典网站..."
    },
    "read_tabs_btn": {
        "en": "Read Tabs",
        "zh": "读取标签页"
    },
    "save_json_btn": {
        "en": "Save as JSON",
        "zh": "保存为JSON"
    },
    "copy_json_btn": {
        "en": "Copy JSON",
        "zh": "复制JSON"
    }
    // Additional strings will be added here
};

// Language management
let currentLanguage = 'en';
const supportedLanguages = ['en', 'zh'];

function setLanguage(lang) {
    if (supportedLanguages.includes(lang)) {
        currentLanguage = lang;
        applyLanguage();
    }
}

function applyLanguage() {
    // Apply translations to all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (i18nStrings[key] && i18nStrings[key][currentLanguage]) {
            el.textContent = i18nStrings[key][currentLanguage];
        }
    });
}

// Initialize language switcher
function initLanguageSwitcher() {
    const switcher = document.createElement('div');
    switcher.className = 'language-switcher';
    switcher.innerHTML = `
        <button class="language-btn">🌐</button>
        <div class="language-dropdown hidden">
            ${supportedLanguages.map(lang => 
                `<button data-lang="${lang}">${lang.toUpperCase()}</button>`
            ).join('')}
        </div>
    `;
    document.body.prepend(switcher);

    // Add event listeners
    switcher.querySelector('.language-btn').addEventListener('click', () => {
        switcher.querySelector('.language-dropdown').classList.toggle('hidden');
    });

    switcher.querySelectorAll('[data-lang]').forEach(btn => {
        btn.addEventListener('click', () => {
            setLanguage(btn.getAttribute('data-lang'));
        });
    });
}