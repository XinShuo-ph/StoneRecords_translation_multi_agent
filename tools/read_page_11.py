from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 11 (0-indexed is 10)
page = reader.pages[10]
text = page.extract_text()
print(f"--- Page 11 ---")
print(text)
