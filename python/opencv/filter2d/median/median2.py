#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# load image (grayscale)
# 入力画像をグレースケールで読み込み
gray = cv.imread(
    "/Users/github/sample/python/opencv/filter2d/median/input.png", 0)

# Spatial filtering
# 方法2
dst = cv.medianBlur(gray, ksize=13)

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/median/output.png", dst)
