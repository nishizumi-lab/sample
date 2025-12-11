import numpy as np

# 5日分の株価データ（例）
price = np.array([100, 102, 101, 105, 110])

# 先頭日の株価
print(price[0])   # 100

# 最終日の株価
print(price[-1])  # 110

# スライスで参照（2～4日目の株価）
print(price[1:4])  # [102 101 105]

# 3日目の株価を修正
price[2] = 999
print(price)  # [100 102 999 105 110]

# 2～4日目の株価を一括で書き換え
price[1:4] = [200, 201, 202]
print(price)  # [100 200 201 202 110]