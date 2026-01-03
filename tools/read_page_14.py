from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 14 (0-indexed is 13)
page = reader.pages[13]
text = page.extract_text()
print(f"--- Page 14 ---")
print(text)
