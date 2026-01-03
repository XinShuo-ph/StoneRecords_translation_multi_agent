from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 12 (0-indexed is 11)
page = reader.pages[11]
text = page.extract_text()
print(f"--- Page 12 ---")
print(text)
