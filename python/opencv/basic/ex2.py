#-*- coding:utf-8 -*-
import cv2
import numpy as np


# 画像の読み込み(RGB)
img = cv2.imread("/Users/github/sample/python/opencv/basic/input.png")

# 三次元配列(カラー)
img2 = np.array([[[36, 28, 237], [ 76, 177, 34], [204, 72, 63]],
                     [[0, 0 ,0], [255, 255, 255], [195, 195, 195]],
                     [[164, 73, 163], [ 36, 28, 237], [0, 0, 0]]])

# 二次元配列（グレースケール）
gray = np.array([[138, 142, 98],
                 [0, 255, 195],
                 [120, 138, 0]])

# 画像ファイルに出力
cv2.imwrite("/Users/github/sample/python/opencv/basic/output1.png", img)
cv2.imwrite("/Users/github/sample/python/opencv/basic/output2.png", img2)
cv2.imwrite("/Users/github/sample/python/opencv/basic/output3.png", gray)