#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread(
    "/Users/github/sample/python/opencv/threshold/dilate_erode/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 二値化処理
gray[gray < 127] = 0
gray[gray >= 127] = 255

# カーネルの定義
kernel = np.ones((6, 6), np.uint8)

# 膨張・収縮処理(方法2)
dilate = cv.dilate(gray, kernel)
erode = cv.erode(dilate, kernel)

# 結果を出力
cv.imwrite(
        "/Users/github/sample/python/opencv/threshold/dilate_erode/dilate.png", dilate)
cv.imwrite(
        "/Users/github/sample/python/opencv/threshold/dilate_erode/erode.png", erode)

