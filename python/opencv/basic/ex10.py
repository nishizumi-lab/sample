#-*- coding:utf-8 -*-
import cv2
import numpy as np

width = 200
height = 100

img = np.zeros((height, width, 3), np.uint8)

# 画像の書き込み
cv2.imwrite("/Users/github/sample/python/opencv/basic/ex10.png", img)
