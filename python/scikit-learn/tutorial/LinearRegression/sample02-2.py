from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# 学習データ（身長[cm]と体重[kg]のペア）
X = np.array([[150], [160], [170], [180], [190]])  # 身長
y = np.array([50, 60, 65, 72, 80])  # 体重

# 学習結果を読み込み
model = joblib.load(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/sample02-1.learn"
)

# 作成したモデルのパラメータを取得
[w] = model.coef_
b = model.intercept_

# パラメータの表示
print("傾き:", w)  # 傾き: 0.7200000000000001
print("切片:", b)  # 切片: -57.000000000000014
print("決定係数:", model.score(X, y))  # 決定係数: 0.9908256880733944

# 体重を予測（身長が175cmの場合）
new_height = np.array([[175]])
predicted_weight = model.predict(new_height)

# 結果表示
print(f"予測体重: {predicted_weight[0]:.1f} kg")  # 予測体重: 69.0 kg
