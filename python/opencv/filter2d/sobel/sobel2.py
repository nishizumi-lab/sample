#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/sobel/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# カーネル（水平、垂直方向の輪郭検出用）
kernel_x = np.array([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]])

kernel_y = np.array([[-1, -2, -1],
                     [0, 0, 0],
                     [1, 2, 1]])

# 方法2
gray_x = cv.filter2D(gray, cv.CV_64F, kernel_x)
gray_y = cv.filter2D(gray, cv.CV_64F, kernel_y)

dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/sobel/output.png", dst)
