# -*- coding: utf-8 -*-
import codecs

# ファイルを開く(読み込みモード)
with open("C:/github/sample/python/file/01_txt/load_data.txt", "r") as f:
    data = f.read()

    # 表示
    print(data)


# ファイルを開く(書き込みモード)
with codecs.open(
    "C:/github/sample/python/file/01_txt/save_data.txt", "w", "utf-8") as f:
    text = "test\tdata\ntest2\tdata2\ntest3\tdata3"
    f.write(text)

