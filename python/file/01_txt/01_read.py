# -*- coding: utf-8 -*-

# ファイルを開く(読み込みモード)
f = open("C:/github/sample/python/file/01_txt/load_data.txt", "r")

data = f.read()

# 表示
print(data)

"""
data.txtの中身
test    data
test2   data2
test3   data3

実行結果
test    data
test2   data2
test3   data3
"""
