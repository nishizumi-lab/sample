# -*- coding: utf-8 -*-
import pandas as pd

data = {
    'miho'  : [158, 82, 56, 84],
    'yukari': [157, 78, 58, 83],
    'saori' : [157, 85, 60, 86]
}

# 日時のインデックス作成
date = pd.date_range("20170201", periods=4)
df = pd.DataFrame(data,index = date)

# 表示
print(df)

"""
【実行結果】

            miho  saori  yukari
2017-02-01   158    157     157
2017-02-02    82     85      78
2017-02-03    56     60      58
2017-02-04    84     86      83
"""