import numpy as np

# 5日分の株価データ
prices = np.array([100, 102, 101, 105, 110])

# for文 + enumerate でインデックスと値を同時に取得
for day, price in enumerate(prices):
    print(f"prices[{day}] = {price}")

# prices[0] = 100
# prices[1] = 102
# prices[2] = 101
# prices[3] = 105
# prices[4] = 110