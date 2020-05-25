# -*- coding: utf-8 -*-
import codecs

filepath = "C:/github/sample/python/file/01_txt/load_data.txt"

# ファイルを開く(読み込みモード)
with codecs.open(filepath, "r", "UTF-8") as f:
    data = f.read()
    # 表示
    print(data)
