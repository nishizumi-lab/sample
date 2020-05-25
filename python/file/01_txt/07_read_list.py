# -*- coding: utf-8 -*-
import codecs

data = []
filepath = "C:/github/sample/python/file/01_txt/load_data.txt"

# ファイルを開く(読み込みモード)
for line in codecs.open(filepath, "r", "UTF-8"):
    line_tmp = line[:-1].strip("\r")
    data += line_tmp.split("\t")

# 表示
print(data)

"""
data.txtの中身
test    data
test2   data2
test3   data3

実行結果
['test    data', 'test2   data2', 'test3   data']
"""
