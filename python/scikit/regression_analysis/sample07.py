# -*- coding: utf-8 -*-
from sklearn import datasets
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

# 相関係数を計算
corr = np.corrcoef(X.T, y)
print(corr)

# 相関係数をヒートマップ化
sns.heatmap(corr, annot=True)
plt.show()