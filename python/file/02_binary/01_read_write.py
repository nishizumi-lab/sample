# -*- coding: utf-8 -*-
filepath = "C:/github/sample/python/file/02_binary/test.dat"

# バイナリモードでファイルに書き込み
with open(filepath, 'wb')  as f:
    f.write(b"saver") # 文字列をバイナリbで保存

# バイナリモードでファイルを読み込み（開く）
with open(filepath, 'rb') as f: 
    data = f.read()
    print(data)  # b'saver'
