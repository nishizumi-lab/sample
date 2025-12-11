import numpy as np

prices = np.array([100, 102, 101, 105, 110])

# for文で100円以上の日を探索
for i, p in enumerate(prices):
    if p >= 100:
        print("100円以上の日:", i)