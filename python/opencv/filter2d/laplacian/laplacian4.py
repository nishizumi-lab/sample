# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/laplacian/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# フィルタ処理
dst = cv.Laplacian(gray, cv.CV_8UC1, ksize=3)

# 2値化処理（大津の方法）
_, binary = cv.threshold(dst, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/laplacian/output4.png", binary)
