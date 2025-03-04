#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/canny/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法2(OpenCVで実装)
dst = cv.Canny(gray, 100, 200)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/canny/output2.png", dst)
