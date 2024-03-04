#-*- coding:utf-8 -*-
import cv2 as cv

# load image (grayscale)
# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/gaussian/input.png")

# convert grayscale
# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# Spatial filtering
# 方法3
dst = cv.GaussianBlur(gray, ksize=(3, 3), sigmaX=1.3)

# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/gaussian/output.png", dst)
