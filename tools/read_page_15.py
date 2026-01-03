from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 15 (0-indexed is 14)
page = reader.pages[14]
text = page.extract_text()
print(f"--- Page 15 ---")
print(text)
