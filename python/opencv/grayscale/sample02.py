#-*- coding:utf-8 -*-
import cv2
import numpy as np

def rgb_to_gray(src):
     # 画像の各チャンネルを分割
     # src(RGBカラー画像)は3次元のNumPy配列(3チャンネル)
     # blue, green, redは2次元のNumPy配列(1チャンネル)
     blue, green, red = src[:,:,0], src[:,:,1], src[:,:,2]

     # R, G, Bの値からGrayの値に変換（float型 → 符号なし8bit整数型に変換）
     # # ここでは、一般的なグレースケール変換の重み付けを使用
     return np.array(0.3 * red + 0.59 * green + 0.11 * blue, dtype='uint8')

# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/grayscale/input.png")

# グレースケール変換
gray = rgb_to_gray(img)

# グレースケール画像の書き込み
cv2.imwrite("C:/github/sample/python/opencv/grayscale/gray2.png", gray)


# BGR, B, G, R, Grayの中身を確認
print("BGR=", img)
print("-------------")

print("Blue=", img[:,:,0])
print("-------------")

print("Green=", img[:,:,1])
print("-------------")

print("Red=", img[:,:,2])
print("-------------")

print("gray=", gray)