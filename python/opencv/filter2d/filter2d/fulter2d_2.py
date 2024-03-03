#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np


def filter2d(src, kernel):
    # カーネルサイズ
    m, n = kernel.shape

    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = src.shape[0], src.shape[1]

    # 出力画像用の配列（要素は全て0）
    dst = np.zeros((h, w))

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 畳み込み演算
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1]*kernel)

    return dst


# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/filter2d/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# カーネル（水平方向の輪郭検出用）
kernel = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

# 畳み込み演算
dst = cv.filter2D(gray, -1, kernel)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/filter2d/output2.png", dst)
