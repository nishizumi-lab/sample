# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# 乱数を100個生成(x, y)
x = np.random.randn(100)
y = np.random.randn(100)

# 散布図
plt.scatter(x,y)

# 表示
plt.grid()
plt.show()