# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import linear_model

# CSVァイルを読み込んでデータフレームに格納
df = pd.read_csv(
    "C:/github/sample/python/scikit/quantification/class1/input.csv")

# 説明変数をダミー変数に変換
x = pd.get_dummies(df[['性別', '文理']])

# 目的変数：満足度
y = df['満足度'].values

# 予測モデルを作成(重回帰)
clf = linear_model.LinearRegression()
clf.fit(x, y)

# 回帰係数と切片の抽出
a = clf.coef_
b = clf.intercept_  

# 回帰係数
print("説明変数：", x) # 
print("回帰係数:", a) # 回帰係数: [-1.  1. -1.  1.]
print("切片:", b)  # 切片: 3.0
print("決定係数:", clf.score(x, y)) # 決定係数: 0.8

"""
説明変数：    性別_女  性別_男  文理_文系  文理_理系
0     0     1      0      1
1     1     0      0      1
2     0     1      1      0
3     1     0      1      0
4     0     1      1      0

回帰係数: [-1.  1. -1.  1.]

切片: 2.9999999999999996

決定係数: 0.8
"""
