# -*- coding: utf-8 -*-

# 検索ワード
keyword = "test"

# ファイルパス
filepath = "C:/github/sample/python/file/sample.txt"

# ファイルの中身を1行ずつ読み込んでリストに格納
with open(filepath, mode='r', newline='', encoding='utf-8') as f_in:
    lines = [line for line in f_in]

# リストから1行文ずつデータを取り出し、検索ワードが含まれているかチェック
for i in lines:
    if keyword in i:
        print("行番号：", lines.index(i+1))  # 行番号： 3

"""
sample.txt

Exdfhsaoipva
vhgsklgha:
nas:glkwnhas:gva]
ashjapghatestdfa
ajslkgahjga
"""