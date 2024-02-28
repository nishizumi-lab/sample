# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as NumPy


# 入力画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/resize/input.png")
    
# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 方法2
dst = cv.resize(
    gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv.INTER_NEAREST)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/resize/nearest2.png", dst)
