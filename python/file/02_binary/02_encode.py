# -*- coding: utf-8 -*-
import base64

filepath = "C:/github/sample/python/file/02_binary/test.bmp"

# ファイルを開く
with open(filepath, "rb") as f:
    data = f.read()

# b64でエンコード
encode = base64.b64encode(data)
print(str(encode))
# エンコードしたデータを保存
with open(filepath + ".b64", "w") as f:
    f.write(str(encode))
