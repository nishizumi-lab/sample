import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import shapiro

# データ読み込み
dataset = pd.read_csv(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/single/dataset01.csv",
    sep=",",
)

# 説明変数と目的変数
X = dataset.loc[:, ["チャンネル登録者数"]].to_numpy()
y = dataset["視聴者数"].to_numpy()

# 相関係数
correlation = np.corrcoef(dataset["チャンネル登録者数"], dataset["視聴者数"])[0, 1]
print("\n■学習済みモデル")
print("相関係数 r:", correlation)

# 線形回帰モデル
model = LinearRegression()

# K分割交差検証（K=5）
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 評価指標の記録用
r2_scores = []
mae_scores = []
rmse_scores = []
all_residuals = []
all_x = []

# 各foldで学習・評価・残差収集
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # 評価指標
    r2_scores.append(r2_score(y_test, y_pred))
    mae_scores.append(mean_absolute_error(y_test, y_pred))
    rmse_scores.append(np.sqrt(mean_squared_error(y_test, y_pred)))

    # 残差収集
    residuals = y_test - y_pred
    all_residuals.extend(residuals)
    all_x.extend(X_test.flatten())

# 結果表示
print("\n■K分割交差検証による汎化性能評価（K=5）")
print("平均 R²:", np.mean(r2_scores))
print("平均 MAE:", np.mean(mae_scores))
print("平均 RMSE:", np.mean(rmse_scores))

# 残差統計
residuals_array = np.array(all_residuals)
print("\n■残差分析")
print("残差の平均:", np.mean(residuals_array))
print("残差の標準偏差:", np.std(residuals_array))

# 正規性検定（Shapiro-Wilk）
stat, p_value = shapiro(residuals_array)
print("\n■Shapiro-Wilk検定（残差の正規性）")
print(f"統計量: {stat:.4f}")
print(f"p値: {p_value:.4f}")
if p_value > 0.05:
    print("→ 残差は正規分布に従う可能性が高い（帰無仮説を棄却できない）")
else:
    print("→ 残差は正規分布に従わない可能性がある（帰無仮説を棄却）")

# 残差プロット
plt.figure(figsize=(12, 5))
plt.rcParams["font.family"] = "MS Gothic"  # 日本語フォントの設定（Windows環境向け）

plt.subplot(1, 2, 1)
plt.scatter(all_x, residuals_array, color="blue", alpha=0.6)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("チャンネル登録者数")
plt.ylabel("残差（実測値 - 予測値）")
plt.title("残差プロット")
plt.grid(True)

# 残差ヒストグラム
plt.subplot(1, 2, 2)
plt.hist(residuals_array, bins=20, color="green", alpha=0.7, edgecolor="black")
plt.xlabel("残差値")
plt.ylabel("頻度")
plt.title("残差のヒストグラム")
plt.grid(True)

plt.tight_layout()
plt.show()
