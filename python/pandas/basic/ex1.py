# -*- coding: utf-8 -*-
import pandas as pd

# リスト作成
data = [158, 157, 157]

# インデックスラベル
index_data = ['miho','saori','yukari']

# リストをSeriesに変換
series = pd.Series(data, index=index_data)
print(series)

"""
miho      158
saori     157
yukari    157

dtype: int64
"""

# ラベルを指定して値を取り出し
print(series["miho"]) # 158