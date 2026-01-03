from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 16 (0-indexed is 15)
page = reader.pages[15]
text = page.extract_text()
print(f"--- Page 16 ---")
print(text)
