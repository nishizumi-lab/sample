#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像とテンプレート画像を取得
img = cv2.imread("C:/github/sample/python/opencv/basic/input2.png")

# 窓画像の左上座標
x, y = 50, 100

# 窓画像の幅・高さ
width, height = 500, 500

# 入力画像から窓画像を切り取り
roi = img[y:y+height, x:x+width]

# 窓画像をグレースケールに変換
roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# グレースケール画像を3チャンネルに変換して元の画像に戻す
img[y:y+height, x:x+width] = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2BGR)

# 変更後の画像を保存
cv2.imwrite("C:/github/sample/python/opencv/basic/ex13.png", img)
