import openpyxl
from openpyxl.cell.cell import Cell\

excel_path = "/Users/github/sample/python/openpyxl/00_sample_data/sample01.xlsx"


#エクセルを読み込む
wb1 = openpyxl.load_workbook(filename=excel_path)
ws1 = wb1['シート1']

wb2 = load_workbook(filename=filepath2)
ws2 = wb1['店舗情報']
セルの取得
for i in range(2, maxRow): #1行目は項目欄なので2行目から取得
    Cell_01 = ws1.cell(i,1)
    Cell_02 = ws1.cell(i,2)
    Cell_03 = ws1.cell(i,3)
    Cell_04 = ws1.cell(i,4)
    Cell_05 = ws1.cell(i,5)

    Cell_01_fill = str(Cell_01.value).zfill(4) #桁を揃える

    ws2[“b1”] = Cell_01_fill
    ws2[“c5”] = Cell_02.value
    ws2[“c6”] = Cell_03.value
    ws2[“f3”] = Cell_04.value
    ws2[“f4”] = Cell_04.value
ファイルの保存
filename = Cell_01_fill + '_' + str(Cell_02.value) + '_v01.xlsx'
wb2.save(filename)

# WorkbookオブジェクトをExcelファイルとして指定したパスに保存
wb.save()