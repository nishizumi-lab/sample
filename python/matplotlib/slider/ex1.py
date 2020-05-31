# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# xとyの値を生成
x = np.arange(1, 5)
y = x

# グラフ描画位置の設定
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.15)
    
# グラフ描画
plt.grid()
graph, = plt.plot(x, y)

def threshold_update(slider_val):
    y = x + slider_val
    # xとyの値を更新
    graph.set_xdata(x)
    graph.set_ydata(y)
    # グラフの再描画
    fig.canvas.draw_idle()
    
# スライダーの表示位置
slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])

# Sliderオブジェクトのインスタンス作成
threshold_slider = Slider(slider_pos, 'd', 0, 2, valinit=0)

# スライダーの値が変更された場合の処理を呼び出し
threshold_slider.on_changed(threshold_update)

# グラフ表示
plt.grid()
plt.show()
