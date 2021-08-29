# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set() # seabornのスタイルをセット

# データセットをロード
dataset = datasets.load_iris()

X = dataset.data  # 説明変数
y = dataset.target # 目的変数
y_name = dataset.target_names # 目的変数に対応する品種名

# 学習用、テスト用にデータを分割（1:1）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

# 学習（ロジスティック回帰 + L1正則化）
clf = linear_model.LogisticRegression(random_state=0, penalty='l1', n_jobs=1, C=15)
clf.fit(X_train, y_train)

# ロジスティック回帰の学習結果
a = clf.coef_
b = clf.intercept_  

print("回帰係数:", a)
print("切片:", b)

# 予測精度の検証
print("スコア(訓練用データを入力):", clf.score(X_train, y_train)) 
print("スコア(テスト用を入力):", clf.score(X_test, y_test)) 

"""
回帰係数: [[ 0.34476547  3.55978285 -4.68014219  0.        ]
 [-0.39624467 -3.89386144  1.34312456 -2.6994755 ]
 [-3.5777949  -1.91844146  6.60045539  6.44262961]]
切片: [  0.          10.9500214  -15.73786262]
スコア(訓練用データを入力): 0.9866666666666667
スコア(テスト用を入力): 0.96
"""