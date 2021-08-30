# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set() # seabornのスタイルをセット

# 糖尿病患者のデータセットをロード
dataset = datasets.load_diabetes()

# 説明変数
X = dataset.data

# 目的変数
y = dataset.target

# 学習用、テスト用にデータを分割（1:1）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

# 予測モデルを作成(重回帰)
clf = linear_model.LinearRegression()

# 学習
clf.fit(X_train, y_train)

# 回帰係数と切片の抽出
a = clf.coef_
b = clf.intercept_  

# 回帰係数
print("回帰係数:", a)
print("切片:", b) 
print("決定係数(学習用):", clf.score(X_train, y_train))
print("決定係数(テスト用):", clf.score(X_test, y_test))

"""
回帰係数: [ -20.41129305 -265.88594023  564.64844662  325.55650029 -692.23796104
  395.62249978   23.52910434  116.37102129  843.98257585   12.71981044]
切片: 154.3589882135515
決定係数(学習用): 0.5730746555685652
決定係数(テスト用): 0.4377492256245158
"""