# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import metrics 
import joblib
import matplotlib.pyplot as plt

# 学習用データのパス
LOAD_TRAIN_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex2_data/train.csv"

# 学習済みモデルデータの保存先パス
SAVE_TRAINED_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex2_data/train.learn"

# 検証用データのパス
LOAD_TEST_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/mlp/ex2_data/test.csv"

# グラフ出力先パス
save_graph_img_path = '/Users/panzer5/github/sample/python/scikit/mlp/ex2_data/graph.png'

# グラフ画像のサイズ
fig_size_x = 10
fig_size_y = 10

# 軸目盛りのフォントサイズ
lim_font_size= 22

# ニューラルネットワークのパラメータ
solver = "sgd"
random_state = 0
max_iter = 10000
    
# 学習用のデータを読み込み
train_data = pd.read_csv(LOAD_TRAIN_DATA_PATH, sep=",")

# 説明変数：x1, x2
train_X = train_data.loc[:, ['x1', 'x2']].values

# 目的変数：x3
train_y = train_data['x3'].values

# 学習
clf = MLPClassifier(
    solver=solver,
    random_state=random_state,
    max_iter=max_iter)

clf.fit(train_X, train_y)

# 学習結果を出力
joblib.dump(clf, SAVE_TRAINED_DATA_PATH)

# 学習済ファイルのロード
clf2 = joblib.load(SAVE_TRAINED_DATA_PATH)

# テスト用データの読み込み
test_data = pd.read_csv(LOAD_TEST_DATA_PATH, sep=",")

# 検証用の説明変数（学習データ）：x1, x2
test_X = test_data.loc[:, ['x1', 'x2']].values

# 検証用の目的変数（正解データ）：x3
test_y = test_data['x3'].values

# 学習結果の検証（テスト用データx1, x2を入力）
predict_y = clf2.predict(test_X)

# 正解データと予測データを比較し、スコアを計算
score = metrics.accuracy_score(test_y, predict_y)

# 検証結果の表示
print("正解データ：", test_y)
print("予測結果：", predict_y)
print("スコア：", score)

"""
正解データ： [0 1 1 0 2 2]
予測結果： [0 1 1 0 2 2]
スコア： 1.0
"""

# 境界線プロット用の格子状データを生成
x1 = np.linspace(0.0, 10.0, 100)
x2 = np.linspace(0.0, 10.0, 100)
X1, X2 = np.meshgrid(x1, x2)    
plot_X = np.c_[X1.ravel(), X2.ravel()]

# 入力
plot_y = clf2.predict(plot_X)

# グラフ設定
plt.figure(figsize=(fig_size_x, fig_size_y))
ax = plt.axes()
plt.rcParams['font.family'] = 'Times New Roman'  # 全体のフォント
plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
plt.rcParams['axes.linewidth'] = 1.0    # 軸の太さ

# 格子データで散布図をプロットし、決定境界を描画（y=0:blue, y=1:red, y=2:green）
plt.scatter(plot_X.T[0][plot_y == 0], plot_X.T[1][plot_y == 0], marker='o', color="blue", alpha=0.1)
plt.scatter(plot_X.T[0][plot_y == 1], plot_X.T[1][plot_y == 1], marker='o', color="red", alpha=0.1)
plt.scatter(plot_X.T[0][plot_y == 2], plot_X.T[1][plot_y == 2], marker='o', color="green", alpha=0.1)

# 学習用データを散布図にプロット（y=0:blue, y=1:red, y=2:green）
plt.scatter(train_X.T[0][train_y == 0], train_X.T[1][train_y == 0], marker='o', label="0", color="blue", alpha=1.0)
plt.scatter(train_X.T[0][train_y == 1], train_X.T[1][train_y == 1], marker='o', label="1", color="red", alpha=1.0)
plt.scatter(train_X.T[0][train_y == 2], train_X.T[1][train_y == 2], marker='o', label="2", color="green", alpha=1.0)


plt.legend(loc=1)           # 凡例の表示（2：位置は第二象限）
plt.title('MLP TEST', fontsize=lim_font_size)   # グラフタイトル
plt.xlabel('x1', fontsize=lim_font_size)            # x軸ラベル
plt.ylabel('x2', fontsize=lim_font_size)            # y軸ラベル

plt.grid()                              # グリッドの表示
# plt.show()
plt.savefig(save_graph_img_path)
plt.close() # バッファ解放
