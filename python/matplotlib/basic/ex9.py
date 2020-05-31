# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

plt.figure()

# 矢印（ベクトル）の始点
X = [0, 1]
Y = [0, 1]
# 矢印（ベクトル）の成分
U = [2, 0.25]
V = [1, 0.5]

# 矢印（ベクトル）
plt.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1)

# グラフ表示
plt.xlim([-1,2])
plt.ylim([-1,2])
plt.grid()
plt.draw()
plt.show()