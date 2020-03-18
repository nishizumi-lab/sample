# -*- coding: utf-8 -*-
import pandas as pd

# -*- coding: utf-8 -*-
import pandas as pd

# 辞書の作成
data = {
    'miho'  : [158, 82, 56, 84],
    'yukari': [157, 78, 58, 83],
    'saori' : [157, 85, 60, 86]
}

# インデックスラベル
index_data = ['身長', 'バスト', '体重', 'ヒップ']

# データフレームの初期化
df = pd.DataFrame(data, index = index_data)

# 表示
print(df)

"""
     miho  yukari  saori
身長    158     157    157
バスト    82      78     85
体重     56      58     60
ヒップ    84      83     86
"""