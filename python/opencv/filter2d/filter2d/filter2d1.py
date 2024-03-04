#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np



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
cv.imwrite("/Users/github/sample/python/opencv/filter2d/filter2d/output1.png", dst)
