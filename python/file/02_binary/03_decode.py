# -*- coding: utf-8 -*-
import base64

filepath = "C:/github/sample/python/file/02_binary/test.bmp"

# ファイルを開く
with open(filepath + ".b64", "r") as f:
    data = f.read()

# b64でデコード     
decode = base64.b64decode(data)

# デコードしたデータを保存
with open(filepath + ".bmp", "wb") as f:
    f.write(decode)
