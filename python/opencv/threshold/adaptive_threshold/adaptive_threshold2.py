#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
    
# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/threshold/adaptive_threshold/input.jpg")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    
# 方法2       
dst = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,13)

    
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/threshold/adaptive_threshold/output.png", dst)