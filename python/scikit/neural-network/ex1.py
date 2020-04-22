# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib

# 学習用データのパス
LOAD_TRAIN_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/neural-network/ex1_data/train.csv"

# 学習済みモデルデータの保存先パス
SAVE_TRAINED_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/svm/ex1_data/train.learn"

# 検証用データのパス
LOAD_TEST_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/svm/ex1_data/test.csv"

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
    solver="sgd",
    random_state=0,
    max_iter=10000)

clf.fit(train_X, train_y)

# 学習結果を出力
joblib.dump(clf, SAVE_TRAINED_DATA_PATH)

# 学習済ファイルのロード
clf2 = joblib.load(SAVE_TRAINED_DATA_PATH)

# テスト用データの読み込み
test_data = pd.read_csv(LOAD_TEST_DATA_PATH, sep=",")

# 学習結果の検証（テスト用データx1, x2を入力）
test_X = test_data.loc[:, ['x1', 'x2']].values
test_y = clf2.predict(test_X)

# 検証結果の表示
print("検証結果：", test_y)

"""
検証結果： [0 1 1 0]
"""
