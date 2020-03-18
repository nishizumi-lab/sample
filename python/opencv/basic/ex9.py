#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像とテンプレート画像をで取得
img = cv2.imread("C:\prog\python\input.png")

# 窓画像の左上座標
x, y = 50, 100

# 窓画像の幅・高さ
w, h = 40, 40

# 窓画像を黒塗り(画素値を0に)
img[y:y+h, x:x+w] = 0

# 画像の書き込み
cv2.imwrite("C:\prog\python\output.png", img)
