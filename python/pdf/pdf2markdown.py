import fitz  # pymupdf
import pandas as pd

# PDFファイルを開く
pdf_document = "https://www.meti.go.jp/policy/safety_security/industrial_safety/sangyo/electric/files/hijyoyohatsudensetsubiFAQ.pdf"
pdf = fitz.open(pdf_document)

# ページを指定してテーブルを抽出
page = pdf.load_page(0)  # 0は最初のページ
tables = page.get_text("dict")["blocks"]

# テーブルをMarkdown形式に変換
for table in tables:
    if "lines" in table:
        df = pd.DataFrame(table["lines"])
        print(df.to_markdown())