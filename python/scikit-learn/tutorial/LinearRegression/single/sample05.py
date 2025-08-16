import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


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
print("\n■学習済みモデル")
print("相関係数 r:", correlation)

# データを訓練用とテスト用に分割（8:2）
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# 線形回帰モデルの学習
model = LinearRegression()
model.fit(x_train, y_train)

# 回帰係数と切片の表示
print("傾き a:", model.coef_[0])
print("切片 b:", model.intercept_)

# テストデータに対する予測
y_pred = model.predict(x_test)

# 汎化性能の評価指標を算出
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n■汎化性能の評価")
print("MAE（平均絶対誤差）:", mae)
print("MSE（平均二乗誤差）:", mse)
print("RMSE（平方平均誤差）:", rmse)
print("R²（決定係数）:", r2)


"""
【実行結果】
■学習済みモデル
相関係数 r: 0.9887097324786042
傾き a: 0.03011362186012872
切片 b: -652.2530190777752

■汎化性能の評価
MAE（平均絶対誤差）: 116.70108243130717
MSE（平均二乗誤差）: 15087.648459286724
RMSE（平方平均誤差）: 122.83178928635178
R²（決定係数）: 0.9762996411258456
"""
