import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

"""
VTuberのチャンネル登録者数と視聴者数の関係を線形回帰モデルで分析・予測するスクリプト。
"""

# 特徴量（説明変数）: VTuberのチャンネル登録者数
X = np.array([[150000], [120000], [100000], [80000]])

# ターゲット変数（目的変数）: 視聴者数
y = np.array([3000, 3100, 2500, 1700])

# 線形回帰モデルを用いて、登録者数と視聴者数の関係を学習
model = LinearRegression()
model.fit(X, y)

# 回帰直線の傾きと切片を出力
print("傾き a:", model.coef_[0])
print("切片 b:", model.intercept_)

# チャンネル登録者数20万人のときの視聴者数を予測
new_subscriber = np.array([[200000]])
predicted_viewers = model.predict(new_subscriber)
print("予測視聴者数:", predicted_viewers[0])

# 予測値（回帰直線上の値）を計算
y_pred = model.predict(X)
residuals = y - y_pred  # 残差

# グラフで可視化
plt.rcParams["font.family"] = "MS Gothic"  # 日本語フォントの設定（Windows環境向け）
plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.scatter(X, y, color="blue", linewidths=3, label="実測値")  # 実測値
plt.plot(X, y_pred, color="red", label="回帰直線")  # 回帰直線

# 残差を描画（垂直線）— 最初の1本だけ凡例を付ける
for i, (xi, yi, ypi) in enumerate(zip(X, y, y_pred)):
    plt.plot(
        [xi[0], xi[0]],
        [yi, ypi],
        color="green",
        linestyle="--",
        linewidth=2,
        label="残差" if i == 0 else None,  # 最初の1本だけラベルを付ける
    )

plt.xlabel("チャンネル登録者数(x)")
plt.ylabel("視聴者数(y)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
