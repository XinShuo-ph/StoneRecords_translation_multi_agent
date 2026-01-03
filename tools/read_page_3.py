from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 3 (0-indexed is 2)
page = reader.pages[2]
text = page.extract_text()
print(f"--- Page 3 ---")
print(text)
