#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像とテンプレート画像をで取得
img = cv2.imread("C:/github/sample/python/opencv/basic/input2.png")

# 窓画像の左上座標
x, y = 50, 100

# 窓画像の幅・高さ
width, height = 500, 500

# 入力画像から窓画像を切り取り
roi = img[y:y+height, x:x+width]

# 窓画像の保存
cv2.imwrite("C:/github/sample/python/opencv/basic/roi.png", roi)