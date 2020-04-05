# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import tree
from sklearn.externals import joblib

LOAD_FILE_PATH = "C:/github/sample/python/scikit/dtc/sample_data/input.csv"
SAVE_FILE_PATH = "C:/github/sample/python/scikit/dtc/sample_data/output.clf"

# CSVファイルを取得
data = pd.read_csv(LOAD_FILE_PATH, sep=",")

# 決定木の分類器を生成
clf = tree.DecisionTreeClassifier()

# 分類器にサンプルデータを入れて学習(説明変数はx1,x2, 目的変数はx3）
clf.fit(data[['x1', 'x2']], data['x3'])

# 学習した分類器で予測
pred = clf.predict(data[['x1', 'x2']])

# 予測結果を表示
print(pred)

"""
[30 25 20 30 45 35 25 35 35 40]
"""