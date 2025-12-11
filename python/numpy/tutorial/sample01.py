import time
import math
import numpy as np

N = 10_000_000

# ============================================
# Pythonリストでの処理
# ============================================
print("=== Pythonリストでの処理 ===")

lst = list(range(N))  # 0〜N-1 の整数を格納したリスト

start = time.time()

# 各要素に対して複数の数学処理を順番に実行
lst_result = [
    math.sin((math.sqrt(x) + 3) * 2)
    for x in lst
]

end = time.time()
print(f"処理時間: {end - start:.4f} 秒")


# ============================================
# NumPy配列での処理
# ============================================
print("\n=== NumPy配列での処理 ===")

arr = np.arange(N)  # 0〜N-1 の整数を格納したNumPy配列

start = time.time()

# NumPy の ufunc によるベクトル化処理
arr_result = np.sin((np.sqrt(arr) + 3) * 2)

end = time.time()
print(f"処理時間: {end - start:.4f} 秒")
