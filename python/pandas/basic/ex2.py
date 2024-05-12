# -*- coding: utf-8 -*-
import pandas as pd

# 辞書の作成
data = {
        'miho'  : [158, 82, 56, 84],
        'yukari': [157, 78, 58, 83],
        'saori' : [157, 85, 60, 86]
}

# データフレームの作成
df = pd.DataFrame(data)
print(df)


"""
【実行結果】

    miho  saori  yukari
0   158    157     157
1    82     85      78
2    56     60      58
3    84     86      83
"""