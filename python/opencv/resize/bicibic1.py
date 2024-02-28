# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

# バイリニア補間法でリサイズ
def resize_bilinear(src, wd, hd):

    # 出力画像用の配列生成（要素は全て空）
    dst = np.empty((hd, wd))

    # 元画像のサイズを取得
    h, w = src.shape[0], src.shape[1]

    # 拡大率を計算
    ax = wd / float(w)
    ay = hd / float(h)

    # バイリニア補間法
    for yd in range(0, hd):
        for xd in range(0, wd):
            x, y = xd/ax, yd/ay
            ox, oy = int(x), int(y)

            # 存在しない座標の処理
            if ox > w - 2:
                ox = w - 2
            if oy > h - 2:
                oy = h - 2

            # 重みの計算
            dx = x - ox
            dy = y - oy

            # 出力画像の画素値を計算
            dst[yd][xd] = (1 - dx) * (1-dy) * src[oy][ox] + dx * (1-dy) * \
                src[oy][ox+1] + (1-dx) * dy * src[oy][ox+1] + \
                dx * dy * src[oy+1][ox+1]

    return dst


# 入力画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/resize/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 方法1(NumPy）
dst = resize_bilinear(gray, gray.shape[1]*2, gray.shape[0]*2)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/resize/bicbic1.png", dst)
