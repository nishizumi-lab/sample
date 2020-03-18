#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 画像の読み込み(RGB)
img = cv2.imread("a.jpg")

height, width, ch = img.shape

# 画素数 = 幅 * 高さ
size = width * height

# 情報表示
print("幅：", width)
print("高さ：", height)
print("チャンネル数:", ch)
print("画素数:", size)   
print("データ型：", img.dtype)

# 1chずつ表示
print("Bの画素値：\n", img[:,:,0])
print("Gの画素値：\n", img[:,:,1])
print("Rの画素値：\n", img[:,:,2])


"""
幅： 3
高さ： 3
チャンネル数: 3
画素数: 9
データ型： uint8

Bの画素値：
 [[ 35  43 221]
 [  0 255 209]
 [200   0   0]]
Gの画素値：
 [[ 12 198  43]
 [  0 255 225]
 [ 87   0   0]]
Rの画素値：
 [[255   0  50]
 [  0 255 226]
 [174 255   0]]
"""