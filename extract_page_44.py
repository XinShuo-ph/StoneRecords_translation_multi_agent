import pdfplumber
import sys

def extract_page_content(pdf_path, page_num):
    with pdfplumber.open(pdf_path) as pdf:
        # page_num is 1-based, pdf.pages is 0-based
        if page_num > len(pdf.pages):
            print(f"Error: Page {page_num} not found")
            return
        
        page = pdf.pages[page_num - 1]
        
        print(f"--- Page {page_num} Content ---")
        
        # Extract text with layout preservation
        text = page.extract_text(layout=True)
        print(text)
        
        print("\n--- Detailed Words ---")
        words = page.extract_words()
        for word in words:
            print(f"Text: {word['text']}, x0: {word['x0']:.2f}, top: {word['top']:.2f}, bottom: {word['bottom']:.2f}, size: {word['bottom']-word['top']:.2f}")

if __name__ == "__main__":
    pdf_path = "红楼梦脂评汇校本_有书签目录_v3.13.pdf"
    page_num = 44
    extract_page_content(pdf_path, page_num)
