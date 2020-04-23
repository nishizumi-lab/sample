# -*- coding: utf-8 -*-
import pandas as pd

LOAD_CSV_PATH = '/Users/panzer5/github/sample/python/pandas/csv/data2.csv'

df_none_usecols = pd.read_csv(LOAD_CSV_PATH, header=None, usecols=[1, 3])
print(df_none_usecols)
#     1   3
# 0  12  14
# 1  22  24
# 2  32  34

df_none_usecols = pd.read_csv('data/src/sample.csv', header=None, usecols=[2])
print(df_none_usecols)
#     2
# 0  13
# 1  23
# 2  33