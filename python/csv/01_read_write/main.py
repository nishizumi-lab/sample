# -*- coding: utf-8 -*-
import csv
import codecs

csv_path = "C:/github/sample/python/csv/01_read_write/data.csv"
data = [[0, 'YUI'],[1, 'UI'],[2, 'MIO']]

# リストのデータをCSVに保存
# Python3系では、open関数で「newline=''」を指定してやらないと空行が発生
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)   

"""
data.csvの中身
0,YUI
1,UI
2,MIO
"""


# CSVをロードしてリストに格納
f = codecs.open(csv_path, "r")
csv_data = [ e for e in csv.reader(f)]
f.close()

print(csv_data)
# [['0', 'YUI'], ['1', 'UI'], ['2', 'MIO']]
