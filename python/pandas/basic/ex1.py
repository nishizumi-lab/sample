# -*- coding: utf-8 -*-
import pandas as pd

# リスト作成
data1 = [158, 157, 157]

# インデックスラベル
index_data = ['miho','saori','yukari']

# リストをSeriesに変換
data2 = pd.Series(data1, index=index_data)
print(data2)

"""
【実行結果】

miho      158
saori     157
yukari    157
dtype: int64
"""