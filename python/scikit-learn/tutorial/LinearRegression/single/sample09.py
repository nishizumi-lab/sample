import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# 予測の不確かさを計算
def predict_with_uncertainty(model, x_train, new_x, se, confidence=0.95):
    new_x = np.array(new_x).flatten()  # ← flattenして1次元にする
    y_pred = model.predict(new_x.reshape(-1, 1))

    n = len(x_train)
    x_mean = np.mean(x_train)
    t_value = stats.t.ppf((1 + confidence) / 2, df=n - 2)

    Sxx = np.sum((x_train.flatten() - x_mean) ** 2)

    # 予測区間の標準誤差（1次元で計算）
    se_pred = se * np.sqrt(1 + 1 / n + ((new_x - x_mean) ** 2 / Sxx))

    lower = y_pred - t_value * se_pred
    upper = y_pred + t_value * se_pred

    return y_pred, lower, upper


# CSVファイルからデータの読み込み
dataset = pd.read_csv(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/single/dataset01.csv",
    sep=",",
)

# 特徴量（説明変数）: VTuberのチャンネル登録者数
x = dataset.loc[:, ["チャンネル登録者数"]].to_numpy()

# ターゲット変数（目的変数）: 視聴者数
y = dataset["視聴者数"].to_numpy()

# 線形回帰モデルを用いて、登録者数と視聴者数の関係を学習
model = LinearRegression()
model.fit(x, y)

# 回帰直線の傾き（登録者数が1人増えるごとの視聴者数の増加量）を出力
print("傾き a:", model.coef_[0])

# 回帰直線の切片（登録者数が0人のときの理論的な視聴者数）を出力
print("切片 b:", model.intercept_)

# 予測値
y_pred = model.predict(x)

# 残差と標準誤差
residuals = y - y_pred
n = len(x)
x_mean = np.mean(x)
se = np.sqrt(np.sum(residuals**2) / (n - 2))

# 予測と不確かさの計算
new_subscriber = np.array([[200000]])  # 20万人の登録者数
y_hat, y_lower, y_upper = predict_with_uncertainty(model, x, new_subscriber, se)

print(f"予測視聴者数: {float(y_hat[0]):.2f}")
print(f"95%予測区間: [{float(y_lower[0]):.2f}, {float(y_upper[0]):.2f}]")

# 可視化
plt.rcParams["font.family"] = "MS Gothic"  # 日本語フォントの設定（Windows環境向け）
plt.figure(figsize=(10, 6))
plt.scatter(x, y, label="実データ", color="gray")
plt.plot(x, y_pred, label="回帰直線", color="blue")

# 予測区間の帯を描画
x_range = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
y_range_pred = model.predict(x_range)
_, y_range_lower, y_range_upper = predict_with_uncertainty(model, x, x_range, se)

plt.fill_between(
    x_range.flatten(),  # x: shape (100,)
    y_range_lower.flatten(),  # y1: shape (100,)
    y_range_upper.flatten(),  # y2: shape (100,)
    color="blue",
    alpha=0.2,
    label="95%予測区間",
)


# 新しい予測点を強調表示
plt.scatter(new_subscriber, y_hat, color="red", label="予測点", zorder=5)
plt.errorbar(
    new_subscriber.flatten(),  # x座標（1次元）
    y_hat.flatten(),  # y座標（1次元）
    yerr=np.array(
        [  # yerrを(2, n)の形にする
            (y_hat - y_lower).flatten(),
            (y_upper - y_hat).flatten(),
        ]
    ),
    fmt="o",
    color="red",
)

plt.xlabel("チャンネル登録者数")
plt.ylabel("視聴者数")
plt.title("視聴者数の予測と不確かさ")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
