# -*- coding: utf-8 -*-
data = []

# ファイルを開く(読み込みモード)
for line in open("C:/github/sample/python/file/01_txt/data.txt", "r"):
    data += line[:-1].split("\t")

# 表示
print(data)

"""
data.txtの中身
test    data
test2   data2
test3   data3

実行結果
['test', 'data', 'test2', 'data2', 'test3', 'data']
"""
