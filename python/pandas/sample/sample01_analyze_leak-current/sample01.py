# -*- coding: utf-8 -*-
import pandas as pd

# CSVファイルのロード
df = pd.read_csv("/Users/github/sample/python/pandas/sample/sample01_analyze_leak-current/data.csv", skiprows = 16)

# データフレームを表示
print(df)

