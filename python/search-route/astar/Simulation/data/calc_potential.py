# -*- coding: utf-8 -*-
import numpy as np

def unique2d(a):
    x = np.array([a[0]])
    for i in xrange(a.shape[0]):
        if np.sum(a[i] - a[i-1]) != 0:
            x = np.append(x, [a[i]], axis=0)
    return np.delete(x, 1, 0)

def main():
    robo = np.loadtxt("path2.csv")
    x,y = robo.T
    o = np.loadtxt("obstacle.csv")
    o = o[::100]
    U=0
    # 壁のポテンシャルを計算
    for i in xrange(o.shape[0]):
        U += 1/np.sqrt((o[i][0]-x)**2+(o[i][1]-y)**2)

    L = np.sum(np.sqrt(np.diff(x)**2+np.diff(y)**2))
    # 各ポテンシャルの重ねあわせ
    print("U=" + str(np.sum(U)) )
    print("u=" + str(np.sum(U)/U.shape[0]) )
    print("L=" + str(L) )
