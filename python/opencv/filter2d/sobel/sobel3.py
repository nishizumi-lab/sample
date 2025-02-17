#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/sobel/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# フィルタ処理
gray_x = cv.Sobel(gray, cv.CV_32F, 1, 0, ksize=3)
gray_y = cv.Sobel(gray, cv.CV_32F, 0, 1, ksize=3)
dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/sobel/output.png", dst)
