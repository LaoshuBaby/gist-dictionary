# Dictionary Tools

This directory contains various tools to help prepare, import, and manipulate dictionary content for the gist-dictionary project.

## Available Tools

### Browser Tab Reader

A tool to extract and process vocabulary from your browser tabs. This tool reads Firefox's existing tabs, sorts them by their actual tab order, retrieves their creation/visiting time, and identifies tabs from dictionary sites.

**Features:**
- Read Firefox's existing tabs
- Sort tabs by their actual tab order
- Get tab creation/visiting time
- Identify tabs from dictionary sites
- Export dictionary site data for gist-dictionary

**Usage:**
```bash
python browser_tab_reader.py --profile-path /path/to/firefox/profile --dict-sites-file dictionary_sites.txt
```

### Anki Import Tool

Convert Anki decks into a format compatible with gist-dictionary.

**Features:**
- Import vocabulary and definitions from Anki decks
- Preserve tags, notes, and example sentences
- Handle media files (audio, images)
- Support for various Anki deck formats

**Usage:** (Coming soon)

### OCR Dictionary Tool

Extract vocabulary and definitions from dictionary app screenshots using Optical Character Recognition (OCR).

**Features:**
- Process screenshots from popular dictionary apps
- Extract word, pronunciation, definition, and examples
- Support for multiple languages
- Batch processing capability

**Dependencies:**
- Tesseract OCR
- Python libraries: pytesseract, opencv-python, pillow

**Usage:** (Coming soon)

### CSV/Excel Converter

Convert vocabulary lists from CSV or Excel files to gist-dictionary format.

**Features:**
- Support for various CSV/Excel formats
- Column mapping configuration
- Batch processing

**Usage:** (Coming soon)

## Planned Tools

- **Web Scraper**: Extract vocabulary from specific websites
- **PDF Extractor**: Extract vocabulary and definitions from PDF dictionaries
- **Audio Processor**: Process and attach audio pronunciations to entries
- **Subtitle Vocabulary Extractor**: Extract vocabulary from movie/TV subtitles

## Contributing

Feel free to contribute to these tools or suggest new ones by opening an issue or pull request.

## License

These tools are released under the same license as the main gist-dictionary project.