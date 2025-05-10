# Dictionary Tools

This directory contains various tools to help prepare, import, and manipulate dictionary content for the gist-dictionary project.

## Available Tools

| Tool ID | Name | Description | Status |
|---------|------|-------------|--------|
| browser_tab_reader | [Browser Tab Reader](browser_tab_reader/) | Extract vocabulary from browser tabs | Available |
| anki_import | [Anki Import Tool](anki_import/) | Convert Anki decks to gist-dictionary format | Planned |
| ocr_dictionary | [OCR Dictionary Tool](ocr_dictionary/) | Extract vocabulary from dictionary app screenshots | Planned |
| csv_excel_converter | [CSV/Excel Converter](csv_excel_converter/) | Convert CSV/Excel vocabulary lists | Planned |

Each tool is contained in its own directory with a dedicated README.md file that includes:
- Feature description
- Usage instructions
- Dependencies

## Installation

Most tools can be used directly without installation, as they are designed to be standalone Python scripts. However, for convenience, you can install them using pip or Poetry.

### Direct Usage (Recommended)

Simply clone the repository and run the Python scripts directly:

```bash
git clone https://github.com/LaoshuBaby/gist-dictionary.git
cd gist-dictionary
python -m tools.browser_tab_reader.browser_tab_reader
```

### Using pip

```bash
# Install a specific tool
pip install -e ".[browser_tab_reader]"
pip install -e ".[ocr_dictionary]"

# Install all tools
pip install -e ".[all]"
```

### Using Poetry (Optional)

If you prefer using Poetry for dependency management:

```bash
# Install the base package
poetry install

# Install with specific tool dependencies
poetry install --extras "browser_tab_reader"
poetry install --extras "ocr_dictionary"

# Install all tool dependencies
poetry install --extras "all"
```

## Contributing

Feel free to contribute to these tools or suggest new ones by opening an issue or pull request.

## License

These tools are released under the same license as the main gist-dictionary project.