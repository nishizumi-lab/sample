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

# 各品種毎に散布図をプロット(各ラベルに50のデータがある)
for i in range(y_name.shape[0]):
    # (がく片の長さ, がく片の幅)でプロット
    plt.plot(X[i*50:i*50+50, 0], X[i*50:i*50+50, 1], 'o')

    # (がく片の長さ, 花弁の長さ)でプロット
    plt.plot(X[i*50:i*50+50, 0], X[i*50:i*50+50, 2], 'o')

    # (がく片の長さ, 花弁の幅)でプロット
    plt.plot(X[i*50:i*50+50, 0], X[i*50:i*50+50, 3], 'o')
    
    plt.title(y_name[i])
    plt.xlabel("X0")
    plt.ylabel("x1, x2, x3")
    plt.grid(True)
    plt.show()