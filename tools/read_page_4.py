from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 4 (0-indexed is 3)
page = reader.pages[3]
text = page.extract_text()
print(f"--- Page 4 ---")
print(text)
