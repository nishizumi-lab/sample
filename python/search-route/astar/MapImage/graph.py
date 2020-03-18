# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

def plot2d(w, p, o, r):
    # グラフ表示
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect="equal")
    # グラフの設定
    ax.tick_params(labelsize=18)        # 軸目盛のフォントサイズ
    ax.set_xlabel("$x$ [m]", fontsize=30, fontname="Times New Roman")   # x軸のラベル
    ax.set_ylabel("$y$ [m]", fontsize=30, fontname="Times New Roman")   # y軸のラベル
    plt.plot(w.T[0],w.T[1],"s", label="Wall", color="#000000")          # 直線を引く
    #plt.plot(o.T[0],o.T[1],"^", label="Obstacle", ms=8,color="#000000")          # 直線を引く
    plt.plot(p.T[0],p.T[1],"ro", label="Route", ms=7)                    # 直線を引く
    plt.plot(r.T[0],r.T[1],"b-", label="Robot",lw=3, alpha=0.7)         # 直線を引く
    plt.xlim([0, 20])
    plt.grid()
    plt.legend(loc=1,fontsize=23)               # 凡例の位置
    plt.ylim([20,0])
    plt.show()              # グラフ表示

def main():

    w = np.loadtxt("wall.csv")
    p = np.loadtxt("path.csv")
    o = np.loadtxt("obst.csv")
    r = np.loadtxt("robot1-1-1.csv")
    plot2d(w, p, o, r)

if __name__ == '__main__':
    main()
