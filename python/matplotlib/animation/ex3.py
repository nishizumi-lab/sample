# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import ctypes
import time


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))


def line000(pos):
    WIDTH = 80
    pl = [(pos) % WIDTH, (pos+1) % WIDTH, (pos+2) % WIDTH]
    rettxt = ""
    for i in range(WIDTH):
        if i in pl:
            rettxt += "0"
        else:
            rettxt += "-"
    return(rettxt)


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
    plt.pause(0.01)     # 更新時間間隔
    plt.clf()           # 画面初期化


ESC = 0x1B          # ESCキーの仮想キーコード
(x, y) = (0, 0)     # 初期値
plt.ion()           # 対話モードオン

while(y != 10):
    realtime_graph(x, y)
    x += 1
    y = x
    if getkey(ESC):     # ESCキーが押されたら終了
        break

plt.close()
