import numpy as np

prices = np.array([100, 102, 101, 105, 110])

# 100円以上の日のインデックスを取得
index = np.where(prices >= 100)

print("100円以上の日:", index[0])  # [0 1 2 3 4]