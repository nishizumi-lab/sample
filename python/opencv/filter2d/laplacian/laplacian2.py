#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/laplacian/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# カーネル（輪郭検出用）
kernel = np.array([[1, 1,  1],
                   [1, -8, 1],
                   [1, 1,  1]])

# フィルタ処理
dst = cv.filter2D(gray, cv.CV_64F, kernel)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/laplacian/output.png", dst)
