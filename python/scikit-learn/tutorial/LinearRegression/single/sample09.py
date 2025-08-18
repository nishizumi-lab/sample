import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression


# ─────────────────────────────────────────────
# 関数：信頼区間と予測区間の計算
# ─────────────────────────────────────────────
def calc_intervals(model, x_train, x_new, se, confidence=0.95):
    x_new = np.array(x_new).flatten()
    y_pred = model.predict(x_new.reshape(-1, 1))

    n = len(x_train)
    x_mean = np.mean(x_train)
    Sxx = np.sum((x_train.flatten() - x_mean) ** 2)
    t = stats.t.ppf((1 + confidence) / 2, df=n - 2)

    # 信頼区間（回帰直線の不確かさ）
    se_conf = se * np.sqrt(1 / n + ((x_new - x_mean) ** 2 / Sxx))
    conf_lower = y_pred - t * se_conf
    conf_upper = y_pred + t * se_conf

    # 予測区間（新しい観測値の不確かさ）
    se_pred = se * np.sqrt(1 + 1 / n + ((x_new - x_mean) ** 2 / Sxx))
    pred_lower = y_pred - t * se_pred
    pred_upper = y_pred + t * se_pred

    return y_pred, conf_lower, conf_upper, pred_lower, pred_upper


# ─────────────────────────────────────────────
# データ読み込みとモデル学習
# ─────────────────────────────────────────────
df = pd.read_csv(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/single/dataset01.csv"
)
x = df[["チャンネル登録者数"]].to_numpy()
y = df["視聴者数"].to_numpy()

model = LinearRegression().fit(x, y)
y_fit = model.predict(x)

# 標準誤差の計算
residuals = y - y_fit
se = np.sqrt(np.sum(residuals**2) / (len(x) - 2))

# ─────────────────────────────────────────────
# 新しい予測点（20万人）と区間の計算
# ─────────────────────────────────────────────
x_new = np.array([[200000]])
y_new, conf_lo, conf_hi, pred_lo, pred_hi = calc_intervals(model, x, x_new, se)

print(f"傾き a: {model.coef_[0]:.4f}")
print(f"切片 b: {model.intercept_:.2f}")
print(f"予測視聴者数: {float(y_new[0]):.2f}")
print(f"95%信頼区間: [{float(conf_lo[0]):.2f}, {float(conf_hi[0]):.2f}]")
print(f"95%予測区間: [{float(pred_lo[0]):.2f}, {float(pred_hi[0]):.2f}]")

# ─────────────────────────────────────────────
# 可視化
# ─────────────────────────────────────────────
plt.rcParams["font.family"] = "MS Gothic"
plt.figure(figsize=(10, 6))

# 実データと回帰直線
plt.scatter(x, y, color="gray", label="実データ")
plt.plot(x, y_fit, color="blue", label="回帰直線")

# 区間の帯（x軸全体に対して）
x_range = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
y_range, conf_lo_range, conf_hi_range, pred_lo_range, pred_hi_range = calc_intervals(
    model, x, x_range, se
)

# 信頼区間（細い帯）
plt.fill_between(
    x_range.flatten(),
    conf_lo_range.flatten(),
    conf_hi_range.flatten(),
    color="green",
    alpha=0.3,
    label="95%信頼区間",
)

# 予測区間（太い帯）
plt.fill_between(
    x_range.flatten(),
    pred_lo_range.flatten(),
    pred_hi_range.flatten(),
    color="blue",
    alpha=0.2,
    label="95%予測区間",
)

# 新しい予測点と誤差バー
plt.scatter(x_new, y_new, color="red", label="予測点", zorder=5)
plt.errorbar(
    x_new.flatten(),
    y_new.flatten(),
    yerr=np.array([(y_new - pred_lo).flatten(), (pred_hi - y_new).flatten()]),
    fmt="o",
    color="red",
)

# 軸とラベル
plt.xlabel("チャンネル登録者数")
plt.ylabel("視聴者数")
plt.title("視聴者数の予測と不確かさ（信頼区間 vs 予測区間）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
