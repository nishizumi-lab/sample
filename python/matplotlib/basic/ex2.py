# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [4, 5, 6, 7, 8]
label_x = ["A","B","C", "D", "E"]

# 中央寄せで棒グラフ作成
plt.bar(x, y, align="center")           
plt.xticks(x, label_x)  # X軸のラベル
plt.show()