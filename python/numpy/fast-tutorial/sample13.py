import numpy as np

# 2次元配列の生成
prices = np.array([[1, 2, 3],
              [4, 5, 6]])

# 二乗の計算（例：データ加工）
new_prices = prices ** 2

# CSVファイルに2次元配列のデータを出力
np.savetxt('C:/github/sample/python/numpy/fast-tutorial/new_data.csv', new_prices, delimiter=",", fmt='%d')