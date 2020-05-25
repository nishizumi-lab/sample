# -*- coding: utf-8 -*-
import codecs

# ファイルを開く(書き込みモード)
f = codecs.open("C:/github/sample/python/file/01_txt/save_data.txt","w","utf-8")

text = "test\tdata\ntest2\tdata2\ntest3\tdata3"

f.write(text)

# ファイルを閉じる
f.close()

"""
■実行結果(data.txtの中身)
test    data
test2   data2
test3   data3
""" 