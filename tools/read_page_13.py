from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 13 (0-indexed is 12)
page = reader.pages[12]
text = page.extract_text()
print(f"--- Page 13 ---")
print(text)
