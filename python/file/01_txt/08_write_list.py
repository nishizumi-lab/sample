# -*- coding: utf-8 -*-
import codecs

data = []
filepath = "C:/github/sample/python/file/01_txt/save_data.txt"

# ファイルを開く(読み込みモード)
for line in codecs.open(filepath, "r", "UTF-8"):
    data += line[:-1].split("\t")

# 表示
print(data)
