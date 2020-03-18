# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt

font = {"family": "IPAexGothic"}
mpl.rc('font', **font)

x = np.array([10, 20, 30, 40])
label = ["沖田", "刑部姫", "アルトリア", "ジャンヌ"]

# 円グラフを描画
plt.pie(x, labels=label, counterclock=False, startangle=90)
plt.show()
