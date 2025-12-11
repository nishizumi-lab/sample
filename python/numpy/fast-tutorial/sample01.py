import time
import math
import numpy as np

#  処理する要素数（ここでは 1,000万）
N = 10000000

#  1. Pythonリストでの処理
# 0〜N-1 の整数を順番に格納した Python のリストを作成
lst = list(range(N))
start = time.time()  # 計測開始

# リスト内包表記で1つずつ処理
lst_result = [
    math.exp(0.000001 * x) * math.sin(x * 0.01) / (1 + (x % 20))
    for x in lst
]

end = time.time()  # 計測終了
print(f"Pythonリストの処理時間: {end - start:.4f} 秒")

#  2. NumPy配列での処理
# 0〜N-1 の整数を連続したメモリ領域に格納した NumPy 配列を生成
arr = np.arange(N)
start = time.time()  # 計測開始

# NumPyの関数で一括で計算
arr_result = np.exp(0.000001 * arr) * np.sin(arr * 0.01) / (1 + (arr % 20))

end = time.time()  # 計測終了
print(f"NumPy配列の処理時間: {end - start:.4f} 秒")