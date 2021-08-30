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

# 説明変数同士の相関係数を計算
corr = np.corrcoef(X.T)
print(corr)

# 相関係数をヒートマップ化
sns.heatmap(corr, annot=True)
plt.show()