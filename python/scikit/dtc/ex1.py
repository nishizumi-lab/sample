# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import tree
import joblib

LOAD_FILE_PATH = "C:/github/sample/python/scikit/dtc/sample_data/input.csv"
SAVE_FILE_PATH = "C:/github/sample/python/scikit/dtc/sample_data/output.clf"

# CSVファイルを取得
data = pd.read_csv(LOAD_FILE_PATH, sep=",")

# 説明変数(x1, x2に設定)
variables = ['x1', 'x2']

# 決定木の分類器を生成
clf = tree.DecisionTreeClassifier()

# 分類器にサンプルデータを入れて学習(目的変数はx）
clf = clf.fit(data[variables], data['x3'])

# 学習結果を出力
with open(SAVE_FILE_PATH, 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

# 保存した学習済ファイルをロード
clf2 = joblib.load(SAVE_FILE_PATH)

# 学習済の分類器で予測
pred2 = clf2.predict(data[['x1', 'x2']])

# 予測結果を表示
print(pred)

# 識別率を表示
print(sum(pred == data['x3']) / len(data[['x1', 'x2']]))
