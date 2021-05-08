# -*- coding: utf-8 -*-
import pandas as pd

# CSVファイルの読み込み
df = pd.read_csv("/Users/github/sample/python/pandas/artoria.csv", index_col=0)

# 計算
count = df['ATK'].count()

# 表示
print("count:",count)
