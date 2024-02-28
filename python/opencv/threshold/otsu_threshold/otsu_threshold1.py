#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像の読み込み
img = cv.imread(
    "/Users/github/sample/python/opencv/threshold/otsu_threshold/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法1 （OpenCVで実装）
ret, th = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

# 結果を出力
cv.imwrite(
    "/Users/github/sample/python/opencv/threshold/otsu_threshold/output.png", th)
