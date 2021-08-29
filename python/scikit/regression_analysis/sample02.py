# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib

# 学習結果を読み込み
clf = joblib.load('C:\prog\python\scikit\clf.learn')

# 回帰係数と切片の抽出
[a] = clf.coef_
b = clf.intercept_ 

# 回帰係数
print("回帰係数:", a) # 回帰係数: -0.0495480955455
print("切片:", b)  # 切片: 20.1197546804