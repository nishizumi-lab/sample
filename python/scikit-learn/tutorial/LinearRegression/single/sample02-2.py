from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# 学習済みモデルの読み込み
model = joblib.load(
    "C:/github/sample/python/scikit-learn/tutorial/LinearRegression/sample02-1.learn"
)

# チャンネル登録者数20万人のときの視聴者数を予測
new_subscriber = np.array([[200000]])

# 予測された視聴者数を表示
predicted_viewers = model.predict(new_subscriber)
print("予測視聴者数:", predicted_viewers[0])

"""
【実行結果】
予測視聴者数: 5662.616822429906
"""
