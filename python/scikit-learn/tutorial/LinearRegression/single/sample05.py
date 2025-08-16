import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


"""
VTuberのチャンネル登録者数と視聴者数の関係を線形回帰モデルで分析・予測するスクリプト。
"""

dataset = pd.read_csv(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/single/dataset01.csv",
    sep=",",
)

# 特徴量（説明変数）: VTuberのチャンネル登録者数
x = dataset.loc[:, ["チャンネル登録者数"]].to_numpy()

# ターゲット変数（目的変数）: 視聴者数
y = dataset["視聴者数"].to_numpy()

# 相関係数を算出
correlation = np.corrcoef(dataset["チャンネル登録者数"], dataset["視聴者数"])[0, 1]
print("相関係数 r:", correlation)

# 線形回帰モデルを用いて、登録者数と視聴者数の関係を学習
model = LinearRegression()
model.fit(x, y)

# 回帰直線の傾き（登録者数が1人増えるごとの視聴者数の増加量）を出力
print("傾き a:", model.coef_[0])

# 回帰直線の切片（登録者数が0人のときの理論的な視聴者数）を出力
print("切片 b:", model.intercept_)

# チャンネル登録者数20万人のときの視聴者数を予測
new_subscriber = np.array([[200000]])

# 予測された視聴者数を表示
predicted_viewers = model.predict(new_subscriber)
print("予測視聴者数:", predicted_viewers[0])

# ✅ 訓練データに対する決定係数（R²）を算出
y_train_pred = model.predict(x)
r2_train = r2_score(y, y_train_pred)
print("訓練データに対する R²（決定係数）:", r2_train)


"""
【実行結果】
相関係数 r: 0.9887097324786042
傾き a: 0.030231000679413776
切片 b: -660.6820828884806
予測視聴者数: 5385.518052994275
訓練データに対する R²（決定係数）: 0.977546935097913　←　訓練データによく適合している
"""
