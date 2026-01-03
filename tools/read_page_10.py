from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 10 (0-indexed is 9)
page = reader.pages[9]
text = page.extract_text()
print(f"--- Page 10 ---")
print(text)
