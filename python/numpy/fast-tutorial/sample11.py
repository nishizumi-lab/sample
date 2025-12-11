import numpy as np

# 5日分の株価データ（例）
prices = np.array([100, 102, 101, 105, 110])

# 平均値
avg = np.average(prices)
print("平均値:", avg)    # 平均値: 103.6

# 中央値
median = np.median(prices)
print("中央値:", median) # 中央値: 102.0

# 分散（値の散らばり）
var = np.var(prices)
print("分散:", var)      # 分散: 13.84

# 標準偏差（変動の大きさ）
std = np.std(prices)
print("標準偏差:", std)  # 標準偏差: 3.720215047547655