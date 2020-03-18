# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [4, 5, 6, 7, 8]
label_x = ["A", "B", "C", "D", "E"]

plt.barh(x, y, align="center")           # 中央寄せで棒グラフ作成
plt.yticks(x, label_x)  # X軸のラベル
plt.show()
