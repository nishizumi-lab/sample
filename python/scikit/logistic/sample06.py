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

# 学習（ロジスティック回帰）
clf = linear_model.LogisticRegression(random_state=0)
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
回帰係数: [[ 0.37664729  1.25055622 -1.94787367 -0.8809699 ]
 [ 0.49723257 -1.6214123   0.31913087 -0.87146961]
 [-1.49621798 -0.59310092  1.90859707  1.70124234]]
切片: [ 0.23856784  0.7342459  -0.86078966]
スコア(訓練用データを入力): 0.92
スコア(テスト用を入力): 0.84
"""