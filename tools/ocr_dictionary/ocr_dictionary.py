#!/usr/bin/env python3
"""
OCR Dictionary Tool - Extract vocabulary from dictionary app screenshots.

This tool uses OCR (Optical Character Recognition) to extract vocabulary and definitions
from dictionary app screenshots.
"""

import argparse
import os
from typing import Dict, List, Optional, Tuple

try:
    import cv2
    import pytesseract
    from PIL import Image
except ImportError:
    print("Error: Required dependencies not found.")
    print("Please install the required dependencies:")
    print("  pip install pytesseract opencv-python pillow")
    print("  or")
    print("  poetry install --extras \"ocr_dictionary\"")
    exit(1)


class OCRDictionary:
    """Extract vocabulary from dictionary app screenshots using OCR."""

    def __init__(self, tesseract_cmd: Optional[str] = None, language: str = "eng"):
        """
        Initialize the OCR Dictionary tool.

        Args:
            tesseract_cmd: Path to the Tesseract executable
            language: OCR language (default: eng)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.language = language

    def process_image(self, image_path: str) -> Dict:
        """
        Process a dictionary app screenshot.

        Args:
            image_path: Path to the screenshot image

        Returns:
            Dictionary containing extracted vocabulary data
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply preprocessing to improve OCR accuracy
        # (This is a placeholder - actual preprocessing would depend on the specific dictionary app)
        # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Perform OCR
        text = pytesseract.image_to_string(gray, lang=self.language)

        # Parse the OCR result to extract vocabulary data
        # (This is a placeholder - actual parsing would depend on the specific dictionary app)
        word, pronunciation, definition = self._parse_ocr_text(text)

        return {
            "word": word,
            "pronunciation": pronunciation,
            "definition": definition,
            "source": os.path.basename(image_path),
        }

    def _parse_ocr_text(self, text: str) -> Tuple[str, str, str]:
        """
        Parse OCR text to extract vocabulary data.

        Args:
            text: OCR text

        Returns:
            Tuple of (word, pronunciation, definition)
        """
        # This is a placeholder implementation
        # Actual parsing would depend on the specific dictionary app
        lines = text.strip().split("\n")
        
        word = lines[0] if lines else ""
        pronunciation = lines[1] if len(lines) > 1 else ""
        definition = "\n".join(lines[2:]) if len(lines) > 2 else ""
        
        return word, pronunciation, definition

    def process_directory(self, directory_path: str) -> List[Dict]:
        """
        Process all images in a directory.

        Args:
            directory_path: Path to directory containing screenshots

        Returns:
            List of dictionaries containing extracted vocabulary data
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        results = []
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        
        for filename in os.listdir(directory_path):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(directory_path, filename)
                try:
                    result = self.process_image(image_path)
                    results.append(result)
                    print(f"Processed: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return results

    def export_to_json(self, results: List[Dict], output_path: str) -> None:
        """
        Export results to a JSON file.

        Args:
            results: List of dictionaries containing extracted vocabulary data
            output_path: Path to output JSON file
        """
        import json
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"Results exported to: {output_path}")


def main():
    """Run the OCR Dictionary tool from the command line."""
    parser = argparse.ArgumentParser(description="Extract vocabulary from dictionary app screenshots")
    parser.add_argument("--image", "-i", help="Path to screenshot image")
    parser.add_argument("--directory", "-d", help="Path to directory containing screenshots")
    parser.add_argument("--output", "-o", default="ocr_results.json", help="Path to output JSON file")
    parser.add_argument("--tesseract", help="Path to Tesseract executable")
    parser.add_argument("--language", "-l", default="eng", help="OCR language (default: eng)")
    
    args = parser.parse_args()
    
    if not args.image and not args.directory:
        parser.error("Either --image or --directory must be specified")
    
    ocr = OCRDictionary(tesseract_cmd=args.tesseract, language=args.language)
    
    if args.image:
        result = ocr.process_image(args.image)
        results = [result]
        print(f"Processed: {args.image}")
    else:
        results = ocr.process_directory(args.directory)
    
    ocr.export_to_json(results, args.output)


if __name__ == "__main__":
    main()