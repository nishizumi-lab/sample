import numpy as np

# 1次元配列の生成（5日分の株価データ）
prices = np.array([100, 102, 101, 105, 110], dtype='int32')
print(prices.dtype)  # int32
print(prices)        # [100 102 101 105 110]

# 2次元配列の生成（2銘柄 × 3日分の株価データ）
# 行：銘柄A・銘柄B
# 列：1日目・2日目・3日目
prices_2d = np.array([[100, 102, 101],   # 銘柄A
                      [ 98, 103,  99]],  # 銘柄B
                     dtype='float32')

print(prices_2d.dtype)  # float32
print(prices_2d)