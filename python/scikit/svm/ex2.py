# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib
import matplotlib.pyplot as plt

# 入力データのファイルパス
load_input_data_path = "/Users/panzer5/github/sample/python/scikit/svm/data/train.csv"

# 学習済みモデルデータの出力先パス
save_trained_data_path = '/Users/panzer5/github/sample/python/scikit/svm/data/train.learn'

# テストデータのファイルパス
load_test_data_path = "/Users/panzer5/github/sample/python/scikit/svm/data/test.csv"

# グラフ出力先パス
save_graph_img_path = '/Users/panzer5/github/sample/python/scikit/svm/data/graph3.png'

# グラフ画像のサイズ
fig_size_x = 10
fig_size_y = 10

# 軸目盛りのフォントサイズ
lim_font_size= 22

# 学習用のデータを読み込み
train_data = pd.read_csv(load_input_data_path, sep=",")

# 説明変数：x1, x2
train_X = train_data.loc[:, ['x1', 'x2']].values

# 目的変数：x3
train_y = train_data['x3'].values

# 学習（SVM）
# kernel = 'linear','rbf','poly','sigmoid'
clf = svm.SVC(gamma=0.01, C=10., kernel='rbf')
clf.fit(train_X, train_y)

# 学習結果を出力
joblib.dump(clf, save_trained_data_path)

# 学習済ファイルのロード
clf2 = joblib.load(save_trained_data_path)

# テスト用データの読み込み
test_data = pd.read_csv(load_test_data_path, sep=",")

# 学習結果の検証（テスト用データx1, x2を入力）
test_X = test_data.loc[:, ['x1', 'x2']].values
test_y = clf2.predict(test_X)

# 検証結果の表示
print("test X：", test_X)
print("test y：", test_y)

"""
test_y： [0 1 1 0]
"""

# 境界線プロット用の格子状データを生成
x1 = np.linspace(0.0, 10.0, 100)
x2 = np.linspace(0.0, 10.0, 100)
X1, X2 = np.meshgrid(x1, x2)    
plot_X = np.c_[X1.ravel(), X2.ravel()]

plot_y = clf2.predict(plot_X)

# 検証結果の表示
print("plot X：", plot_X)
print("plot y：", plot_y)

# グラフ設定
plt.figure(figsize=(fig_size_x, fig_size_y))
ax = plt.axes()
plt.rcParams['font.family'] = 'Times New Roman'  # 全体のフォント
plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
plt.rcParams['axes.linewidth'] = 1.0    # 軸の太さ

# 格子データで散布図をプロットし、決定境界を描画（y=0:blue, y=1:red）
plt.scatter(plot_X.T[0][plot_y <= 0], plot_X.T[1][plot_y <= 0], marker='o', color="blue", alpha=0.2)
plt.scatter(plot_X.T[0][plot_y > 0], plot_X.T[1][plot_y > 0], marker='o', color="red", alpha=0.2)

# 学習用データを散布図にプロット（y=0:blue, y=1:red）
plt.scatter(train_X.T[0][train_y <= 0], train_X.T[1][train_y <= 0], marker='o', color="blue", alpha=1.0)
plt.scatter(train_X.T[0][train_y > 0], train_X.T[1][train_y > 0], marker='o', color="red", alpha=1.0)

#plt.legend(loc=1)           # 凡例の表示（2：位置は第二象限）
#plt.title('SVM TEST', fontsize=lim_font_size)   # グラフタイトル
plt.xlabel('x1', fontsize=lim_font_size)            # x軸ラベル
plt.ylabel('x2', fontsize=lim_font_size)            # y軸ラベル

plt.grid()                              # グリッドの表示
# plt.show()
plt.savefig(save_graph_img_path)
plt.close() # バッファ解放