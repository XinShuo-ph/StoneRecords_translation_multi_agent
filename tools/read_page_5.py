from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
# Page 5 (0-indexed is 4)
page = reader.pages[4]
text = page.extract_text()
print(f"--- Page 5 ---")
print(text)
