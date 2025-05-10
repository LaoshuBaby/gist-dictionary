# OCR Dictionary Tool

Extract vocabulary and definitions from dictionary app screenshots using Optical Character Recognition (OCR).

## Features

- Process screenshots from popular dictionary apps
- Extract word, pronunciation, definition, and examples
- Support for multiple languages
- Batch processing capability
- Export results to JSON format for gist-dictionary

## Requirements

- Python 3.6+
- Tesseract OCR (must be installed separately)
- Python packages:
  - pytesseract
  - opencv-python
  - pillow

## Installation

### 1. Install Tesseract OCR

#### Windows
1. Download and install Tesseract from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add the Tesseract installation directory to your PATH environment variable

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
# For additional languages
sudo apt install tesseract-ocr-all
```

### 2. Install Python Dependencies

```bash
# Direct installation
pip install pytesseract opencv-python pillow

# Using Poetry
poetry install --extras "ocr_dictionary"
```

## Usage

### Basic Usage

```bash
# Process a single image
python ocr_dictionary.py --image path/to/screenshot.png

# Process all images in a directory
python ocr_dictionary.py --directory path/to/screenshots/

# Specify output file
python ocr_dictionary.py --image path/to/screenshot.png --output results.json
```

### Advanced Options

```bash
# Specify Tesseract executable path (if not in PATH)
python ocr_dictionary.py --image path/to/screenshot.png --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Specify language (default is English)
python ocr_dictionary.py --image path/to/screenshot.png --language eng+fra
```

## Supported Dictionary Apps

The OCR tool is designed to work with screenshots from various dictionary applications, including:

- Merriam-Webster
- Oxford Dictionary
- Cambridge Dictionary
- Collins Dictionary
- Dictionary.com
- Custom dictionary apps (may require configuration)

## How It Works

1. The tool loads the screenshot image
2. It preprocesses the image to improve OCR accuracy
3. Tesseract OCR extracts text from the image
4. The extracted text is parsed to identify word, pronunciation, and definition
5. Results are exported to JSON format compatible with gist-dictionary

## Limitations

- OCR accuracy depends on image quality and clarity
- Different dictionary apps may have different layouts requiring custom parsing
- Some special characters or phonetic symbols may not be recognized correctly
- Performance may vary based on the Tesseract version and language packs installed

## Integration with gist-dictionary

The output JSON file can be imported into gist-dictionary to add the extracted vocabulary to your collection.

## Troubleshooting

- If Tesseract is not found, specify the path using the `--tesseract` option
- For poor OCR results, try improving the screenshot quality or adjusting the preprocessing parameters
- Make sure the appropriate language packs are installed for Tesseract

## Future Improvements

- Add support for more dictionary apps
- Improve parsing accuracy with machine learning
- Add GUI interface for easier use
- Support for extracting example sentences and related words