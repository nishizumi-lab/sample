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

    """
    【実行結果】
    ■学習済みモデル
    相関係数 r: 0.9887097324786042

    ■K分割交差検証による汎化性能評価（K=5）
    R²（決定係数）: [0.97629964 0.96205125 0.98038493 0.87306545 0.98674433]
    平均 R²: 0.9557091220054488
    MAE（平均絶対誤差）: [116.70108243 161.71079631 111.89684449 193.62444962  58.47853996]
    平均 MAE: 128.4823425620885
    RMSE（平方平均誤差）: [122.83178929 182.7842319  115.491323   210.27570805  76.95164515]
    平均 RMSE: 141.6669394778975
    """
