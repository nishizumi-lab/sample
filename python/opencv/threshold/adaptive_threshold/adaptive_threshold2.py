#-*- coding:utf-8 -*-
import cv2
import numpy as np
    
# 入力画像を読み込み
img = cv2.imread("C:/github/sample/python/opencv/threshold/input.jpg")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
# 方法2       
dst = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

    
# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/threshold/output.png", dst)