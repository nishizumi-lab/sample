# -*- coding: utf-8 -*-
import codecs

filepath = "C:/github/sample/python/file/01_txt/save_data.txt"

# ファイルを開く(書き込みモード)
f = open(filepath,"w")

text = "test\tdata\ntest2\tdata2\ntest3\tdata3"

f.write(text)

# ファイルを閉じる
f.close()

"""
save_data.txtの中身
test    data
test2   data2
test3   data3
""" 
