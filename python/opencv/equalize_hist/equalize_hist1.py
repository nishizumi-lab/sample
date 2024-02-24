#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/equalize_hist/input.jpg")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法1(OpenCVで実装)
dst = cv.equalizeHist(gray)

# 結果の出力
cv.imwrite("/Users/github/sample/python/opencv/equalize_hist/output1.jpg", dst)
