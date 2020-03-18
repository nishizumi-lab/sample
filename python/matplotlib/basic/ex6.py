# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# 乱数を100個生成
x = np.random.randn(100)

# ヒストグラムの描画
plt.hist(x, bins=20, color='g', width=0.3)
plt.show()
