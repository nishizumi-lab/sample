# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model
import joblib

# CSVファイルの読み込み
data = pd.read_csv('C:/github/sample/python/scikit/regression_analysis/data.csv', sep=',')

# 回帰モデルの呼び出し
clf = linear_model.LinearRegression()

# 説明変数にx1とx2のデータを使用
X = data.loc[:, ['x1', 'x2']].values

# 目的変数にx3のデータを使用
Y = data['x3'].values

# 予測モデルを作成（重回帰）
clf.fit(X, Y)

# 回帰係数と切片の抽出
a = clf.coef_
b = clf.intercept_  

# 回帰係数
print("回帰係数:", a) # 回帰係数: [ 0.70068905 -0.64667957]
print("切片:", b) # 切片: 12.184694815481187
print("決定係数:", clf.score(X, Y)) # 決定係数: 0.6624246214760455

# 学習結果を出力
joblib.dump(clf, 'C:/github/sample/python/scikit/regression_analysis/multiple.learn') 
