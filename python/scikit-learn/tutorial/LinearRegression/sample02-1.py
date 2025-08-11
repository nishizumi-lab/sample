from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# 学習データ（身長[cm]と体重[kg]のペア）
X = np.array([[150], [160], [170], [180], [190]])  # 身長
y = np.array([50, 60, 65, 72, 80])  # 体重

# 線形回帰モデルを作成・学習
model = LinearRegression()
model.fit(X, y)

# 学習結果をファイルに保存
joblib.dump(
    model,
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/sample02-1.learn",
)
