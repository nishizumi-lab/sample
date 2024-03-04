#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# load image (grayscale)
# 入力画像をグレースケールで読み込み
gray = cv.imread("/Users/github/sample/python/opencv/filter2d/blur/input.png", 0)

# Spatial filtering
# 方法3(OpenCVで実装)
dst = cv.blur(gray, ksize=(3, 3))

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/blur/output.png", dst)
