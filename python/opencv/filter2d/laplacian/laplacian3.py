#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/laplacian/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# フィルタ処理
dst = cv.Laplacian(gray, cv.CV_32F, ksize=3)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/laplacian/output.png", dst)
