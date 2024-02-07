#-*- coding:utf-8 -*-
import cv2
import numpy as np


# 画像の読み込み(RGB)
img = cv2.imread("/Users/github/sample/python/opencv/basic/input.png")

# 画像の読み込み(グレースケール)
gray = cv2.imread("/Users/github/sample/python/opencv/basic/input.png", 0)

# 画像の読み込み(RGBA)
rgba = cv2.imread("/Users/github/sample/python/opencv/basic/input.png", -1)

# 画素値の表示
print("rgb=", img)
print("\n------------------------\n")
print("gray=", gray)
print("\n------------------------\n")
print("rgba=", rgba)

'''
rgb= [[[ 36  28 237] [ 76 177  34] [204  72  63]]
　　　 [[  0   0   0] [255 255 255] [195 195 195]]
　　　 [[164  73 163] [ 36  28 237] [  0   0   0]]]

------------------------

gray= [[138 142  98]
         [  0 255 195]
         [120 138   0]]

------------------------

rgba= [[[ 36  28 237 255] [ 76 177  34 255] [204  72  63 255]]
         [[  0   0   0 255] [255 255 255 255] [195 195 195 255]]
         [[164  73 163 255] [ 36  28 237 255] [  0   0   0 255]]]
'''