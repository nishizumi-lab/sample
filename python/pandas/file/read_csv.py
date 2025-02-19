# -*- coding: utf-8 -*-
import pandas as pd

LOAD_CSV_PATH = '/Users/panzer5/github/sample/python/pandas/csv/data2.csv'

# デフォルト
# 連番が自動で付与されインデックスになる
df = pd.read_csv(LOAD_CSV_PATH)
print("df")
print(df)

"""
    A   B   C
0  11  21  31
1  12  22  32
2  13  23  33
"""

# インデックスの列番号を1に指定（index_col=1）
# 2列目Bがインデックス扱い
df1 = pd.read_csv(LOAD_CSV_PATH, index_col=1)
print("df1")
print(df1)
"""
     A   C
B         
21  11  31
22  12  32
23  13  33
"""

# インデックスなし（index_col=None）
# 連番が自動で付与されインデックスになる
df2 = pd.read_csv(LOAD_CSV_PATH, index_col=None)
print("df2")
print(df2)
"""
    A   B   C
0  11  21  31
1  12  22  32
2  13  23  33
"""

# ヘッダーなし（header=None）
# 連番が自動で付与されヘッダーになる
df4 = pd.read_csv(LOAD_CSV_PATH, header=None)
print("df4")
print(df4)
"""
    0   1   2
0   A   B   C
1  11  21  31
2  12  22  32
3  13  23  33
"""

# usecols=[0, 1]で1, 2列目のみ取り出し
df5 = pd.read_csv(LOAD_CSV_PATH, usecols=[0, 2])
print("df5")
print(df5)
"""
    A   C
0  11  31
1  12  32
2  13  33
"""

# usecols=[2]で3列目のみ取り出し
df6 = pd.read_csv(LOAD_CSV_PATH, usecols=[2])
print("df6")
print(df6)
"""
   C
0  31
1  32
2  33
"""

# usecols=list(range(0,3))で1〜3列目のみ取り出し
df7 = pd.read_csv(LOAD_CSV_PATH, usecols=list(range(0,3)))
print("df7")
print(df7)
"""
   A   B   C
0  11  21  31
1  12  22  32
2  13  23  33
"""

# 2行目までスキップして取り出し
df8 = pd.read_csv(LOAD_CSV_PATH, skiprows=2)
print("df8")
print(df8)
"""
   12  22  32
0  13  23  33
"""
