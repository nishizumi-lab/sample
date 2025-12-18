import time
import cmath
import numpy as np
print(np.__version__)
#  処理する要素数（ここでは 1,000万）
N = 10000000

#  1. Pythonリストでの処理
lst = list(range(N))
start = time.time()

# オイラーの公式で計算
lst_result = [
    cmath.exp(1j * x)
    for x in lst
]

end = time.time()
print(f"Pythonリストの処理時間: {end - start:.4f} 秒")

#  2. NumPy配列での処理
arr = np.arange(N)
start = time.time()

# オイラーの公式で計算
arr_result = np.exp(1j * arr)

end = time.time()
print(f"NumPy配列の処理時間: {end - start:.4f} 秒")