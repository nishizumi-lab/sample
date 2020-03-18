#-*- coding:utf-8 -*-
import cv2
import numpy as np


# 入力画像の読み込み
img = cv2.imread("C:\prog\python\\test\input.jpg")

# 方法2(OpenCVで実装)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 結果を出力
cv2.imwrite("C:\prog\python\\test\hsv.jpg", hsv)
