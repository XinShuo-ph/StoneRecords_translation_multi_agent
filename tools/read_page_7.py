from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 7 (0-indexed is 6)
page = reader.pages[6]
text = page.extract_text()
print(f"--- Page 7 ---")
print(text)
