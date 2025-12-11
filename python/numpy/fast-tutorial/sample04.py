import numpy as np

# 3日分の株価データ（例）
prices1 = np.array([100, 102, 101])  # 銘柄A
prices2 = np.array([98, 103, 99])    # 銘柄B

# 加算（2銘柄の株価を単純合計）
print(prices1 + prices2)  # [198 205 200]

# 減算（株価差）
print(prices1 - prices2)  # [ 2 -1  2]

# 乗算（要素ごとの積：ポートフォリオ比率計算などで利用）
print(prices1 * prices2)  # [9800 10506  9999]

# 除算（株価比：相対的な強さの比較）
print(prices1 / prices2)  # [1.02040816 0.99029126 1.02020202]

# 剰余（あまり：整数データの処理で利用）
print(prices1 % prices2)  # [2 102  2]

# 冪乗（例：株価の2乗）
print(prices1 ** 2)      # [10000 10404 10201]

# 符号反転
print(-prices1)          # [-100 -102 -101]