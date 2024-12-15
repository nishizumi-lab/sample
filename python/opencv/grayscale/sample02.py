#-*- coding:utf-8 -*-
import cv2
import numpy as np

def rgb_to_gray(src):
     # チャンネル分解
     b, g, r = src[:,:,0], src[:,:,1], src[:,:,2]

     # R, G, Bの値からGrayの値に変換（float型 → 符号なし8bit整数型に変換）
     return np.array(0.3 * r + 0.59 * g + 0.11 * b, dtype='uint8')

# 入力画像の読み込み
img = cv2.imread("C:\prog\python\input.png")

# グレースケール変換
gray = rgb_to_gray(img)

# グレースケール画像の書き込み
cv2.imwrite("C:\prog\python\gray.png", gray)


# BGR, B, G, R, Grayの2次元配列を確認
print("BGR=", img)
print("-------------")

print("Blue=", img[:,:,0])
print("-------------")

print("Green=", img[:,:,1])
print("-------------")

print("Red=", img[:,:,2])
print("-------------")
print("gray=", gray)