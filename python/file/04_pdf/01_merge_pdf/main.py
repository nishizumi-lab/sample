from pathlib import Path
import PyPDF2

# ロードするPDFファイルのパスと文字コード
load_pdf_dir = "/Users/github/sample/python/file/04_pdf/00_sample_data"
encode_type = "UTF-8"
pdf_files = Path(load_pdf_dir)

# 結合したPDFの保存先パス
merge_pdf_path = "/Users/github/sample/python/file/04_pdf/00_result_data"

pdf_files = pdf_files.glob("*.pdf")
print(pdf_files)
#pdf_files = sorted(pdf_dir)

# １つのPDFファイルにまとめる
pdf_writer = PyPDF2.PdfFileWriter()
for pdf_file in pdf_files:
    pdf_reader = PyPDF2.PdfFileReader(str(pdf_file))
    for i in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(i))

# 保存ファイル名（先頭と末尾のファイル名で作成）
merged_file = pdf_files[0].stem + "-" + pdf_files[-1].stem + ".pdf"

# 保存
with open(merged_file, "wb") as f:
    pdf_writer.write(f)

"""
C:/github/sample/python/file/03_csv/01_list_to_dir/内に以下のディレクトリが作成されます。

1-A組
2-B組
3-C組
4-D組
5-E組
"""