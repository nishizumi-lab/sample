# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def realtime_graph(x, y):
    line, = plt.plot(x, y, "ro", label="y=x")  # (x,y)のプロット
    line.set_ydata(y)   # y値を更新
    plt.title("Graph")  # グラフタイトル
    plt.xlabel("x")     # x軸ラベル
    plt.ylabel("y")     # y軸ラベル
    plt.legend()        # 凡例表示
    plt.grid()          # グリッド表示
    plt.xlim([0, 10])    # x軸範囲
    plt.ylim([0, 10])    # y軸範囲
    plt.draw()          # グラフの描画
    plt.pause(0.5) # 0.5sec間隔で更新
    plt.clf()  # 画面初期化
    

(x, y) = (0, 0)     # 初期値
plt.ion()           # 対話モードオン

while(y != 10):
    realtime_graph(x, y)
    x += 1
    y = x

plt.close()  # 画面を閉じる
