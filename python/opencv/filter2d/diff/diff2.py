#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像を読み込み
img = cv2.imread("/Users/github/sample/python/opencv/filter2d/diff/input.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# カーネル（水平、垂直方向の輪郭検出用）
kernel_x = np.array([[0, -1, 0],
                     [0, 0, 0],
                     [0, 1, 0]])

kernel_y = np.array([[0, 0, 0],
                    [-1, 0, 1],
                    [0, 0, 0]])

# 方法2
gray_x = cv2.filter2D(gray, cv2.CV_64F, kernel_x)
gray_y = cv2.filter2D(gray, cv2.CV_64F, kernel_y)

dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

# 結果を出力
cv2.imwrite("/Users/github/sample/python/opencv/filter2d/diff/output.png", dst)
