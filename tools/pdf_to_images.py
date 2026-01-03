#!/usr/bin/env python3
"""
Extract PDF pages as images for AI workers to read directly.

Usage:
    python3 pdf_to_images.py source.pdf output_dir/ [start_page] [end_page]
    
Examples:
    # Extract all pages
    python3 pdf_to_images.py 红楼梦脂评汇校本.pdf source_pages/
    
    # Extract pages 15-28 (Chapter 1)
    python3 pdf_to_images.py 红楼梦脂评汇校本.pdf source_pages/ 15 28

Requirements:
    pip install pdf2image
    
    Also requires poppler:
    - Ubuntu/Debian: sudo apt-get install poppler-utils
    - macOS: brew install poppler
    - Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases
"""

import sys
import os
from pathlib import Path

def extract_pages(pdf_path: str, output_dir: str, start_page: int = None, end_page: int = None):
    """Extract PDF pages as PNG images."""
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image not installed. Run: pip install pdf2image")
        print("Also ensure poppler is installed on your system.")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading PDF: {pdf_path}")
    
    # Convert pages
    if start_page and end_page:
        print(f"Extracting pages {start_page} to {end_page}...")
        pages = convert_from_path(
            pdf_path, 
            first_page=start_page, 
            last_page=end_page,
            dpi=150  # Good balance of quality and size
        )
        page_offset = start_page - 1
    else:
        print("Extracting all pages...")
        pages = convert_from_path(pdf_path, dpi=150)
        page_offset = 0
    
    # Save each page
    for i, page in enumerate(pages):
        page_num = i + page_offset + 1
        output_path = os.path.join(output_dir, f"page_{page_num:04d}.png")
        page.save(output_path, "PNG")
        print(f"  Saved: {output_path}")
    
    print(f"\nDone! Extracted {len(pages)} pages to {output_dir}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 pdf_to_images.py <pdf_file> <output_dir> [start_page] [end_page]")
        print("\nExamples:")
        print("  python3 pdf_to_images.py source.pdf output/")
        print("  python3 pdf_to_images.py source.pdf output/ 15 28")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    start_page = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end_page = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    extract_pages(pdf_path, output_dir, start_page, end_page)


if __name__ == "__main__":
    main()
