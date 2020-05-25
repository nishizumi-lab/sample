# -*- coding: utf-8 -*-

filepath = "C:/github/sample/python/file/01_txt/load_data.txt"

# ファイルを開く(読み込みモード)
with open(filepath, "r") as f:
    data = f.read()
    # 表示
    print(data)

