# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import metrics 
import joblib

# 学習用データのパス
LOAD_TRAIN_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex1_data/train.csv"

# 学習済みモデルデータの保存先パス
SAVE_TRAINED_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex1_data/train.learn"

# 検証用データのパス
LOAD_TEST_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex1_data/test.csv"

# ニューラルネットワークのパラメータ
solver = "sgd"
random_state = 0
max_iter = 10000
    
# 学習用のデータを読み込み
train_data = pd.read_csv(LOAD_TRAIN_DATA_PATH, sep=",")

# 説明変数：x1, x2
train_X = train_data.loc[:, ['x1', 'x2']].values

# 目的変数：x3
train_y = train_data['x3'].values

# 学習
clf = MLPClassifier(
    solver=solver,
    random_state=random_state,
    max_iter=max_iter)

clf.fit(train_X, train_y)

# 学習結果を出力
joblib.dump(clf, SAVE_TRAINED_DATA_PATH)

# 学習済ファイルのロード
clf2 = joblib.load(SAVE_TRAINED_DATA_PATH)

# テスト用データの読み込み
test_data = pd.read_csv(LOAD_TEST_DATA_PATH, sep=",")

# 検証用の説明変数（学習データ）：x1, x2
test_X = test_data.loc[:, ['x1', 'x2']].values

# 検証用の目的変数（正解データ）：x3
test_y = test_data['x3'].values

# 学習結果の検証（テスト用データx1, x2を入力）
predict_y = clf2.predict(test_X)

# 正解データと予測データを比較し、スコアを計算
score = metrics.accuracy_score(test_y, predict_y)

# 検証結果の表示
print("正解データ：", test_y)
print("予測結果：", predict_y)
print("スコア：", score)

"""
正解データ： [0 1 1 0 2 2]
予測結果： [0 1 1 0 2 2]
スコア： 1.0
"""
