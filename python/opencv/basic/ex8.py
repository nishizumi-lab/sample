#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像とテンプレート画像をで取得
img = cv2.imread("C:\prog\python\input.png")

# 窓画像の左上座標
x, y = 50, 100

# 窓画像の幅・高さ
w, h = 40, 40

# 入力画像から窓画像を切り取り
roi = img[y:y+h, x:x+w]

# 窓画像の保存
cv2.imwrite("C:\prog\python\output.png", roi)
