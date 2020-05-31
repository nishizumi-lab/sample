# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

plt.figure()

# 矢印（ベクトル）の成分
U = [0.5,0.25,-0.5]
V = [0.25,0.5,-0.25]

# 矢印（ベクトル）
plt.quiver(U,V,angles='xy',scale_units='xy',scale=1)

# z,y軸の設定
plt.xlim([-1,3])
plt.ylim([-1,3])

# グラフ描画
plt.grid()
plt.draw()
plt.show()