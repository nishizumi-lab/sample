# -*- coding: utf-8 -*-
import cv2
import numpy as NumPy

# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/resize/input.png")
    
# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 方法2(OpenCV)
dst = cv2.resize(
    gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv2.INTER_CUBIC)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/resize/bicibic2.png", dst)
