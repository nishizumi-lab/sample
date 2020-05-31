# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# データを用意
x = [1, 2, 3, 3, 3, 4, 4, 5, 6]

# ヒストグラムの描画
plt.hist(x, bins=6, color='g', width=0.3)
plt.show()
