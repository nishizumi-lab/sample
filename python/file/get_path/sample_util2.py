# -*- coding: uTf-8 -*-
from util2.file.searcher import FileSearcher
import ntpath

fsearch = FileSearcher()

# 検索対象のパス
LOAD_DIR_PATH = "C:/github/sample/python/file/get_path/sample_data/"

# 検索結果の出力先
paths = fsearch.get_paths(LOAD_DIR_PATH)


print(paths['file_abs_path'])
"""
['C:/github/sample/python/file/get_path/sample_data/\\a.txt', 'C:/github/sample/python/file/get_path/sample_data/\\b.txt',
    'C:/github/sample/python/file/get_path/sample_data/c\\d.txt']
"""

for cnt, path in enumerate(paths['file_abs_path']):
    print("count：", cnt + 1)
    print("path：", path)
    print("dirname：", ntpath.dirname(path))
    print("basename：", ntpath.basename(path))
    print("ext：", ntpath.splitext(path)[1])
    print("ext2：", ntpath.splitext(path)[1][1:])
    print("filename：", ntpath.splitext(ntpath.basename(path))[0])
    print("----------------")

"""
----------------
count： 1
path： C:/github/sample/python/file/get_path/sample_data/\a.txt
dirname： C:/github/sample/python/file/get_path/sample_data
basename： a.txt
ext： .txt
ext2： txt
----------------
count： 2
path： C:/github/sample/python/file/get_path/sample_data/\b.txt
dirname： C:/github/sample/python/file/get_path/sample_data
basename： b.txt
ext： .txt
ext2： txt
----------------
path： C:/github/sample/python/file/get_path/sample_data/c\d.txt
dirname： C:/github/sample/python/file/get_path/sample_data/c
basename： d.txt
ext： .txt
ext2： txt
----------------
PS C:\Users\panzer4> & C:/Users/panzer4/AppData/Local/Programs/Python/Python38-32/python.exe c:/github/sample/python/file/get_path/sample_util2.py
['C:/github/sample/python/file/get_path/sample_data/\\a.txt', 'C:/github/sample/python/file/get_path/sample_data/\\b.txt', 'C:/github/sample/python/file/get_path/sample_data/c\\d.txt']
count： 1
path： C:/github/sample/python/file/get_path/sample_data/\a.txt
dirname： C:/github/sample/python/file/get_path/sample_data
basename： a.txt
ext： .txt
ext2： txt
filename： a
----------------
count： 2
path： C:/github/sample/python/file/get_path/sample_data/\b.txt
dirname： C:/github/sample/python/file/get_path/sample_data
basename： b.txt
ext： .txt
ext2： txt
filename： b
----------------
count： 3
path： C:/github/sample/python/file/get_path/sample_data/c\d.txt
dirname： C:/github/sample/python/file/get_path/sample_data/c
basename： d.txt
ext： .txt
ext2： txt
filename： d
----------------
"""
