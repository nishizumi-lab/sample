from sklearn.linear_model import LinearRegression
import numpy as np

# 学習データ（身長[cm]と体重[kg]のペア）
X = np.array([[150], [160], [170], [180], [190]])  # 身長
y = np.array([50, 60, 65, 72, 80])  # 体重

# 線形回帰モデルを作成・学習
model = LinearRegression()
model.fit(X, y)

# 予測したい身長（例：175cm）
new_height = np.array([[175]])
predicted_weight = model.predict(new_height)

# 結果表示
print(f"予測体重: {predicted_weight[0]:.1f} kg")  # 予測体重: 69.0 kg
