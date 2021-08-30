# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib

# 学習用のデータを読み込み
train_data = pd.read_csv("C:/github/sample/python/scikit/svm/ex1_data/train.csv", sep=",")

# 説明変数：x1, x2
train_X = train_data.loc[:, ['x1', 'x2']].values

# 目的変数：x3
train_y = train_data['x3'].values

# 学習（SVM）
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(train_X, train_y)

# 学習結果を出力
joblib.dump(clf, 'C:/github/sample/python/scikit/svm/ex1_data/train.learn')

# 学習済ファイルのロード
clf2 = joblib.load('C:/github/sample/python/scikit/svm/ex1_data/train.learn')

# テスト用データの読み込み
test_data = pd.read_csv("C:/github/sample/python/scikit/svm/ex1_data/test.csv", sep=",")

# 学習結果の検証（テスト用データx1, x2を入力）
test_X = test_data.loc[:, ['x1', 'x2']].values
test_y = clf2.predict(test_X)

# 検証結果の表示
print("検証結果：", test_y)

"""
検証結果： [0 1 1 0]
"""
