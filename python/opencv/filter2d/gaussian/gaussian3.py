#-*- coding:utf-8 -*-
import cv2

# load image (grayscale)
# 入力画像を読み込み
img = cv2.imread("C:/github/sample/python/opencv/filter2d/gaussian/input.png")

# convert grayscale
# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Spatial filtering
# 方法3
dst = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=1.3)

# output
# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/filter2d/gaussian/output.png", dst)
