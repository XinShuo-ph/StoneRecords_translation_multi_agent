from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 9 (0-indexed is 8)
page = reader.pages[8]
text = page.extract_text()
print(f"--- Page 9 ---")
print(text)
