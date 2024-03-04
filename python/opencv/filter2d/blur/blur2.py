#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# load image (grayscale)
# 入力画像をグレースケールで読み込み
gray = cv.imread("/Users/github/sample/python/opencv/filter2d/blur/input.png", 0)

# kernel of blur filter
# カーネル（縦方向の輪郭検出用）
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])

# Spatial filtering
# 方法2(OpenCVで実装)
dst = cv.filter2D(gray, -1, kernel)

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/blur/output.png", dst)
