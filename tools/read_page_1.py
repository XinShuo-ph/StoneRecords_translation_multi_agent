from pypdf import PdfReader

reader = PdfReader("红楼梦脂评汇校本_有书签目录_v3.13.pdf")
page = reader.pages[0]
text = page.extract_text()
print(text)
