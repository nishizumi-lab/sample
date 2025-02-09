#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# load image (grayscale)
# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/gaussian/input.png")

# convert grayscale
# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# kernel of gaussian
# カーネル
kernel = np.array([[1/16, 1/8, 1/16],
                   [1/8, 1/4, 1/8],
                   [1/16, 1/8, 1/16]])

# Spatial filtering
# フィルタ処理
dst = cv.filter2D(gray, -1, kernel)

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/gaussian/output.png", dst)
