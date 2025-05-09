# Browser Tab Reader

A tool to extract and process vocabulary from your browser tabs. This tool reads Firefox's existing tabs, sorts them by their actual tab order, retrieves their creation/visiting time, and identifies tabs from dictionary sites.

## Features

- Read Firefox's existing tabs from session files
- Sort tabs by their actual tab order (window and tab index)
- Get tab creation and last accessed time
- Identify tabs from dictionary sites
- Extract search terms from dictionary URLs
- Export dictionary site data for gist-dictionary

## Requirements

- Python 3.6 or higher
- Firefox browser with an active profile

## Installation

### Using Poetry

```bash
# Install with Poetry
poetry install --extras "browser_tab_reader"

# Or install all tools
poetry install --extras "all"
```

### Using pip

```bash
pip install -e ".[browser_tab_reader]"
```

### Manual Installation

No special installation is required. Just make sure you have Python 3.6+ installed.

## Usage

### Basic Usage

```bash
python browser_tab_reader.py
```

This will automatically find your Firefox profile and use a default list of dictionary sites.

### Advanced Usage

```bash
python browser_tab_reader.py --profile-path /path/to/firefox/profile --dict-sites-file dictionary_sites.txt --output dictionary_tabs.json
```

### Parameters

- `--profile-path`: Path to Firefox profile directory (optional, will auto-detect if not specified)
- `--dict-sites-file`: File containing dictionary site domains, one per line (optional, will use default list if not specified)
- `--output`: Output file for dictionary tabs in JSON format (optional, will print to console if not specified)

## Dictionary Sites File Format

The dictionary sites file should contain one domain per line. For example:

```
dictionary.com
merriam-webster.com
vocabulary.com
thefreedictionary.com
dictionary.cambridge.org
```

## Sample Usage

A sample usage script is provided to demonstrate how the browser tab reader works:

```bash
python sample_usage.py
```

This script creates a sample Firefox profile with some tabs, including dictionary sites, and shows how the browser tab reader processes them.

## How It Works

1. The tool locates Firefox profile directories on your system
2. It reads session data from `sessionstore.js` or `sessionstore-backups/recovery.js`
3. It extracts tab information including URL, title, creation time, and last accessed time
4. It checks if each tab is from a dictionary site
5. For dictionary sites, it attempts to extract the search term from the URL
6. It outputs the results to the console or a JSON file

## Limitations

- The tool can only read Firefox tabs, not other browsers
- It relies on Firefox's session files, which might change format in future Firefox versions
- It can only extract search terms from known dictionary site URL patterns
- It cannot access the actual content of the tabs, only the URL and metadata

## Integration with gist-dictionary

The output of this tool can be used to populate your gist-dictionary with words you've looked up in online dictionaries. The JSON output includes the search term, URL, and timestamp information that can be imported into gist-dictionary.

## Troubleshooting

If the tool cannot find your Firefox profile:
1. Use `--profile-path` to specify the path manually
2. Check if Firefox is installed and has been run at least once
3. Look for the profile directory in:
   - Linux: `~/.mozilla/firefox/`
   - macOS: `~/Library/Application Support/Firefox/Profiles/`
   - Windows: `%APPDATA%\Mozilla\Firefox\Profiles\`