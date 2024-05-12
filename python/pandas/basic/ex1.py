# -*- coding: utf-8 -*-
import pandas as pd


# ①リストからSeriesを作成
list_data = [158, 157, 157]
index_data = ['miho','saori','yukari']

series = pd.Series(list_data, index=index_data)
print(series)

"""
miho      158
saori     157
yukari    157

dtype: int64
"""

# ラベルを指定して値を取り出し
print(series["miho"]) # 158

# ②辞書からSeriesを作成
dict_data = {'miho': 158, 'saori': 157, 'yukari': 157}



# リストからSeriesに変換
series2 = pd.Series(dict_data)
print(series2)

"""
miho      158
saori     157
yukari    157

dtype: int64
"""
