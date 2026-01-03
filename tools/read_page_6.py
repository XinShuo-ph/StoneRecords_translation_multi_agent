from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 6 (0-indexed is 5)
page = reader.pages[5]
text = page.extract_text()
print(f"--- Page 6 ---")
print(text)
