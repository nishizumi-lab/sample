# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# (x, y, z)
x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]
z = [1, 2, 3, 4, 5]

# 3Dでプロット
fig = plt.figure()
ax = Axes3D(fig)
ax.plot(x, y, z, "o-", color="#00aa00", ms=4, mew=0.5)

# 軸ラベル
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# 表示
plt.show()
