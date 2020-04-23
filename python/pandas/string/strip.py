# -*- coding: utf-8 -*-
import pandas as pd

LOAD_CSV_PATH = '/Users/panzer5/github/sample/python/pandas/csv/data3.csv'

# デフォルト
df1 = pd.read_csv(LOAD_CSV_PATH)
print("df1")
print(df1)

"""
   A    B    C
0   11   21   31
1   12   22   32
2  *13  *23  *33
3   14   24   34
"""

# *を除去
df2 = pd.read_csv(LOAD_CSV_PATH)
df2 = df2.replace(r"\*", "", regex=True)
print(df2)
"""
     A    B    C
0   11   21   31
1   12   22   32
2  *13  *23  *33
3   14   24   34
"""

