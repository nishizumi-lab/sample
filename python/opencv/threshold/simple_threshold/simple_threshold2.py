#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 閾値
threshold_value = 127

# 入力画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/threshold/simple_threshold/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法2 （OpenCVで実装）
ret, threshold_img = cv.threshold(gray, threshold_value, 255, cv.THRESH_BINARY)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/threshold/simple_threshold/output.png", threshold_img)