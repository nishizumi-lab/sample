# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

x = np.array([10, 20, 30, 40])
labels = ["Okita", "Osakabe", "Altiria", "Jannue"]
colors = ["r", "g", "b", "m"] # ラベル毎の色を指定

# 円グラフを描画
plt.pie(x, labels=labels, colors=colors, autopct="%1.1f%%", counterclock=True, startangle=90)
plt.legend(labels, fontsize=12, loc=1) # (7)凡例の表示
plt.show()