# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib

# CSVファイルのパス（学習用）
LOAD_CSV_PATH = "C:/github/sample/python/scikit/logistic/sample_data/input.csv"

# CSVファイルのパス（検証用）
LOAD_TEST_PATH = "C:/github/sample/python/scikit/logistic/sample_data/test.csv"

# CLFファイルのパス（学習済ファイル用）
SAVE_CLF_PATH = "C:/github/sample/python/scikit/logistic/sample_data/train.clf"

# 学習用のデータを読み込み
data = pd.read_csv("C:/github/sample/python/scikit/logistic/sample_data/input.csv", sep=",")

# 説明変数：x1, x2
X = data.loc[:, ['x1', 'x2']].values

# 目的変数：x3
y = data['x3'].values

# 学習（ロジスティック回帰）
clf = linear_model.LogisticRegression(random_state=0)
clf.fit(X, y)

# 学習結果を出力
joblib.dump(clf, SAVE_CLF_PATH)

# 学習済ファイルのロード
clf2 = joblib.load(SAVE_CLF_PATH)

# ロジスティック回帰の学習結果
a = clf2.coef_
b = clf2.intercept_  
print("回帰係数:", a) # 回帰係数: [[-0.02217148  0.31554403]]
print("切片:", b)     # 切片: [-1.06960241]
print("決定係数:", clf2.score(X, y)) # 決定係数: 0.818181818182

# テスト用データの読み込み
data = pd.read_csv(LOAD_TEST_PATH, sep=",")

# 学習結果の検証（テスト用データx1, x2を入力）
X_test = data.loc[:, ['x1', 'x2']].values
y_predict = clf.predict(X_test)

# 検証結果の表示
print("検証結果：", y_predict)

"""
回帰係数: [[0.79826198 0.94551053]]
切片: [-8.71899451]
決定係数: 0.9090909090909091
検証結果 ： [0110]
"""


