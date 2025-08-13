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
y = np.array([4000, 3100, 2500, 1700])

# 線形回帰モデルを用いて、登録者数と視聴者数の関係を学習
model = LinearRegression()
model.fit(X, y)

# 回帰直線の傾き（登録者数が1人増えるごとの視聴者数の増加量）を出力
print("傾き a:", model.coef_[0])

# 回帰直線の切片（登録者数が0人のときの理論的な視聴者数）を出力
print("切片 b:", model.intercept_)

# チャンネル登録者数20万人のときの視聴者数を予測
new_subscriber = np.array([[200000]])

# 予測された視聴者数を表示
predicted_viewers = model.predict(new_subscriber)
print("予測視聴者数:", predicted_viewers[0])

# グラフで可視化
plt.rcParams["font.family"] = "MS Gothic"  # 日本語フォントの設定（Windows環境向け）
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)  # x軸ラベルの数値にカンマを入れる
plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)  # y軸ラベルの数値にカンマを入れる
plt.scatter(X, y, color="blue", label="実測値")
plt.plot(X, model.predict(X), color="red", label="回帰直線")
plt.xlabel("チャンネル登録者数")
plt.ylabel("視聴者数")
plt.title("視聴者数の単回帰分析")
plt.legend()
plt.grid(True)
plt.show()


"""
【実行結果】
傾き a: 0.03242990654205607
切片 b: -823.3644859813076
予測視聴者数: 5662.616822429906
"""
