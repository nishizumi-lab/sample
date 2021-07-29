#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像を読み込み
img = cv2.imread("C:/github/sample/python/opencv/equalize_hist/input.jpg")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 方法2(OpenCVで実装)
dst = cv2.equalizeHist(gray)

# 結果の出力
cv2.imwrite("C:/github/sample/python/opencv/equalize_hist/output1.jpg", dst)
