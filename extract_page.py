#!/usr/bin/env python3
"""Extract a single page from PDF"""
import sys
import fitz  # PyMuPDF

pdf_path = sys.argv[1]
page_num = int(sys.argv[2]) - 1  # 0-indexed

doc = fitz.open(pdf_path)
page = doc[page_num]

# Extract text
text = page.get_text()
print("=== Page Text ===")
print(text)
print("\n=== Saving image ===")

# Save as image
pix = page.get_pixmap(dpi=150)
img_path = f"source_pages/page_{page_num+1:04d}.png"
pix.save(img_path)
print(f"Saved: {img_path}")

doc.close()
