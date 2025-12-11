import numpy as np

# CSVファイルを読み込み（区切り文字はカンマ）
prices = np.genfromtxt('C:/github/sample/python/numpy/fast-tutorial/data.csv', delimiter=',')

# 配列の中身を確認
print(prices)
# [[ 1.  2.  3.  4.]
#  [ 5.  6.  7.  8.]
#  [ 9. 10. 11. 12.]]