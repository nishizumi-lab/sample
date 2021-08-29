# -*- coding: utf-8 -*-
from sklearn import datasets
import matplotlib.pyplot as plt
import seaborn as sns

sns.set() # seabornのスタイルをセット

# 糖尿病患者のデータセットをロード
dataset = datasets.load_diabetes()

# 説明変数
X = dataset.data

# 目的変数
y = dataset.target

for i in range(X.shape[1]):
    plt.plot(X[:, i], y, 'o')

plt.xlabel("X")
plt.ylabel("y")
plt.grid(True)
plt.show()