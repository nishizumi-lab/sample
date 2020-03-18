# -*- coding: utf-8 -*-
import numpy as np
import cv2

# ミニチュア画像に変換
def miniature(img, sk=2.5):
    # HSVに変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 彩度を上げる
    hsv[:,:,1] = hsv[:,:,1] * sk

    # BGRに戻す
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 画像の高さ、幅、チャンネル数を取得
    h, w, ch = img.shape

    # 上下をぼかす
    img[0:int(h/3), :] = cv2.blur(img[0:int(h/3), :], ksize=(5, 5))
    img[int(h/3):int(h/2), :] = cv2.blur(img[int(h/3):int(h/2), :], ksize=(4, 4))    
    img[int(h/2):int(h*2/3), :] = cv2.blur(img[int(h/2):int(h*2/3), :], ksize=(3, 3))
    img[int(h*10/11):h, :] = cv2.blur(img[int(h*10/11):h, :], ksize=(3, 3))  

    return img


# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/sample_data/input2.jpg")

# ミニチュア画像化（彩度を上げる倍率：2.3）
img2 = miniature(img, 2.3)

# 結果を出力
cv2.imwrite(
    "C:/github/sample/python/opencv/miniature_filter/ex1.jpg", img2)


