# -*- coding: utf-8 -*-
import pandas as pd

LOAD_CSV_PATH = '/Users/panzer5/github/sample/python/pandas/csv/data2.csv'

# デフォルト
# 連番が自動で付与されインデックスになる
df = pd.read_csv(LOAD_CSV_PATH)
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
print(df2)
"""
    A   B   C
0  11  21  31
1  12  22  32
2  13  23  33
"""

# ヘッダーなし（header=None）
# 連番が自動で付与されヘッダーになる
df4 = pd.read_csv(LOAD_CSV_PATH, header=None, usecols=[0, 1])
print(df4)
"""
    0   1
0   A   B
1  11  21
2  12  22
3  13  23
"""

# usecols=[0, 1]で1, 2列目のみ取り出し
df5 = pd.read_csv(LOAD_CSV_PATH, usecols=[0, 1])
print(df5)
"""
    A   B
0  11  21
1  12  22
2  13  23
"""

# usecols=[0, 1]で1, 2列目のみ取り出し
df6 = pd.read_csv(LOAD_CSV_PATH, usecols=[2])
print(df6)
"""
    C
0   C
1  31
2  32
3  33
"""