# -*- coding: utf-8 -*-
import codecs

filepath = "C:/github/sample/python/file/01_txt/save_data.txt"

# ファイルを開く(書き込みモード)
with codecs.open(filepath, "w", "utf-8") as f:
    text = "test\tdata\ntest2\tdata2\ntest3\tdata3"
    f.write(text)

