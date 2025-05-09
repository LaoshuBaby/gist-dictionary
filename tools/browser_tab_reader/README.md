# Browser Tab Reader

A tool to extract and process vocabulary from your browser tabs. This tool reads Firefox's existing tabs, sorts them by their actual tab order, retrieves their creation/visiting time, and identifies tabs from dictionary sites.

## Features

- Read Firefox's existing tabs
- Sort tabs by their actual tab order
- Get tab creation/visiting time
- Identify tabs from dictionary sites
- Export dictionary site data for gist-dictionary

## Usage

```bash
python browser_tab_reader.py --profile-path /path/to/firefox/profile --dict-sites-file dictionary_sites.txt
```

See the detailed [browser_tab_reader_README.md](browser_tab_reader_README.md) for more information.

## Dependencies

- Python 3.6+
- No external dependencies required for basic functionality