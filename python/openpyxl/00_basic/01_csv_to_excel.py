import csv
import openpyxl

csv_path = "/Users/github/sample/python/openpyxl/00_sample_data/sample01.csv"
excel_path = "/Users/github/sample/python/openpyxl/00_sample_data/sample01.xlsx"

wb = openpyxl.Workbook()
ws = wb.active
 
with open(csv_path) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        ws.append(row)
 
wb.save(excel_path)