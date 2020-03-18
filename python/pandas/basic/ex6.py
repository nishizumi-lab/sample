# -*- coding: utf-8 -*-
import pandas as pd

# データフレームの初期化
df = pd.DataFrame({
    '名前': ['西住みほ', '秋山優花里', '武部沙織', '五十鈴華', '冷泉麻子'],
    '身長': [158, 157, 157, 163, 145]},
    index=['車長', '装填手', '通信手', '砲手', '操縦手']
)

# データフレームをCSVファイルに書き込む
df.to_csv("C:/github/sample/python/pandas/basic/anko.csv")

# データフレームをExcelファイルに書き込む
df.to_excel("C:/github/sample/python/pandas/basic/anko.xls")

# CSVファイルの読み込み
df_csv = pd.read_csv(
    "C:/github/sample/python/pandas/basic/anko.csv", index_col=0)

# 表示
print(df_csv)

"""
        名前   身長
車長    西住みほ  158
装填手  秋山優花里  157
通信手   武部沙織  157
砲手    五十鈴華  163
操縦手   冷泉麻子  145
"""

# Excelファイルの読み込んでデータフレームに格納
df_excel = pd.read_excel("C:/github/sample/python/pandas/basic/anko.xls")

# 表示
print(df_excel)
"""
  Unnamed: 0     名前   身長
0         車長   西住みほ  158
1        装填手  秋山優花里  157
2        通信手   武部沙織  157
3         砲手   五十鈴華  163
4        操縦手   冷泉麻子  145
"""