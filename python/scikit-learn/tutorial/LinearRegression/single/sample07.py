import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import (
    make_scorer,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

"""
VTuberのチャンネル登録者数と視聴者数の関係を線形回帰モデルで分析・予測するスクリプト。
"""

# データ読み込み
dataset = pd.read_csv(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/single/dataset01.csv",
    sep=",",
)

# 特徴量（説明変数）: VTuberのチャンネル登録者数
X = dataset.loc[:, ["チャンネル登録者数"]].to_numpy()

# ターゲット変数（目的変数）: 視聴者数
y = dataset["視聴者数"].to_numpy()

# 相関係数を算出
correlation = np.corrcoef(dataset["チャンネル登録者数"], dataset["視聴者数"])[0, 1]
print("\n■学習済みモデル")
print("相関係数 r:", correlation)

# 線形回帰モデル
model = LinearRegression()

# ✅ K分割交差検証（K=5）
cv = KFold(n_splits=5, shuffle=True, random_state=42)

# ✅ 各評価指標を交差検証で算出
r2_scores = cross_val_score(model, X, y, cv=cv, scoring=make_scorer(r2_score))
mae_scores = cross_val_score(
    model, X, y, cv=cv, scoring=make_scorer(mean_absolute_error)
)
mse_scores = cross_val_score(
    model, X, y, cv=cv, scoring=make_scorer(mean_squared_error)
)
rmse_scores = np.sqrt(mse_scores)

# ✅ 結果表示
print("\n■K分割交差検証による汎化性能評価（K=5）")
print("R²（決定係数）:", r2_scores)
print("平均 R²:", np.mean(r2_scores))
print("MAE（平均絶対誤差）:", mae_scores)
print("平均 MAE:", np.mean(mae_scores))
print("RMSE（平方平均誤差）:", rmse_scores)
print("平均 RMSE:", np.mean(rmse_scores))
