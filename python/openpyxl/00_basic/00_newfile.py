import openpyxl

# 1.Excelファイルを作成し、その中のシート名を「sheet_A」に修正
# 新規に空のWorkbookオブジェクトを生成
wb = openpyxl.Workbook()

# ワークブックのアクティブなシートを取得
sheet = wb.active

# アクティブなシート名を「sheet_A」に変更
sheet.title = 'sheet_A'

# WorkbookオブジェクトをExcelファイルとして指定したパスに保存
wb.save('/Users/github/sample/python/openpyxl/00_sample_data/newbook.xlsx')