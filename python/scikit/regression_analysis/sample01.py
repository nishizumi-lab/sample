# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model
import joblib

# データ読み込み
data = pd.read_csv('C:/github/sample/python/scikit/regression_analysis/data.csv', sep=',')

# 線形回帰モデル
clf = linear_model.LinearRegression()

# 説明変数xに "x1"のデータを使用
x = data.loc[:, ['x1']].values

# 目的変数yに "x2"のデータを使用
y = data['x2'].values

# 予測モデルを作成（単回帰）
clf.fit(x, y)

# パラメータ（回帰係数、切片）を抽出
[a] = clf.coef_
b = clf.intercept_  

# パラメータの表示
print("回帰係数:", a)
print("切片:", b) 
print("決定係数:", clf.score(x, y))

# 学習結果の出力
joblib.dump(clf, 'C:/github/sample/python/scikit/regression_analysis/clf.learn') 

"""
回帰係数: -0.0495480955455
切片: 20.1197546804
決定係数: 0.109433563543
"""