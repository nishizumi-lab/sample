#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/roberts/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# カーネル（斜方向の輪郭検出用）
kernel_x = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, -1]])

kernel_y = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, -1]])
# フィルタ処理
gray_x = cv.filter2D(gray, cv.CV_64F, kernel_x)
gray_y = cv.filter2D(gray, cv.CV_64F, kernel_y)

dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/roberts/output.png", dst)
