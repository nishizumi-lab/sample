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

# 学習（ロジスティック回帰 + L2正則化）
clf = linear_model.LogisticRegression(random_state=0, penalty='l2', n_jobs=1, C=15)
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
回帰係数: [[ 0.66524407  2.15628389 -3.42581672 -1.5952244 ]
 [ 0.27279333 -3.08293152  0.91970137 -2.27832851]
 [-3.39992172 -1.51071288  4.65769737  4.0098312 ]]
切片: [ 0.40883009  5.77538438 -3.89572019]
スコア(訓練用データを入力): 0.9866666666666667
スコア(テスト用を入力): 0.92
"""