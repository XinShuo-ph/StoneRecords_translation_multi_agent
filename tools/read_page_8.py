from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 8 (0-indexed is 7)
page = reader.pages[7]
text = page.extract_text()
print(f"--- Page 8 ---")
print(text)
