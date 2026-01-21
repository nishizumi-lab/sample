import numpy as np

# 2 × 3 の空配列を生成（初期化されていないため中身は不定）
prices = np.empty((2, 3), dtype='float32')

print(prices)
# 例：
# [[0.         0.         0.        ]
# [0.         0.         0.06643876]]