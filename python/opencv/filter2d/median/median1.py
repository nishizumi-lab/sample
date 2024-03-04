#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np


def median_filter(src, ksize):
    # 畳み込み演算をしない領域の幅
    # width of skip
    d = int((ksize-1)/2)
    h, w = src.shape[0], src.shape[1]

    # ndarray of destination
    # 出力画像用の配列（要素は入力画像と同じ）
    dst = src.copy()

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 近傍にある画素値の中央値を出力画像の画素値に設定
            dst[y][x] = np.median(src[y-d:y+d+1, x-d:x+d+1])

    return dst


# load image (grayscale)
# 入力画像をグレースケールで読み込み
gray = cv.imread("/Users/github/sample/python/opencv/filter2d/median/input.png", 0)

# Spatial filtering
# 方法1
dst = median_filter(gray, ksize=5)

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/median/output.png", dst)
