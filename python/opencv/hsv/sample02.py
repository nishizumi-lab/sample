#-*- coding:utf-8 -*-
import cv2
import numpy as np


def rgb_to_hsv(src, ksize=3):
    # 高さ・幅・チャンネル数を取得
    h, w, c = src.shape

    # 入力画像と同じサイズで出力画像用の配列を生成(中身は空)
    dst = np.empty((h, w, c))

    for y in range(0, h):
        for x in range(0, w):
            # R, G, Bの値を取得して0～1の範囲内にする
            [b, g, r] = src[y][x]/255.0

            # R, G, Bの値から最大値と最小値を計算
            mx, mn = max(r, g, b), min(r, g, b)

            # 最大値 - 最小値
            diff = mx - mn

            # Hの値を計算
            if mx == mn : h = 0
            elif mx == r : h = 60 * ((g-b)/diff)
            elif mx == g : h = 60 * ((b-r)/diff) + 120
            elif mx == b : h = 60 * ((r-g)/diff) + 240
            if h < 0 : h = h + 360

            # Sの値を計算
            if mx != 0:s = diff/mx
            else: s = 0

            # Vの値を計算
            v = mx

            # Hを0～179, SとVを0～255の範囲の値に変換
            dst[y][x] = [h * 0.5, s * 255, v * 255]

    return dst


# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/hsv/input.png")

# 方法1(NumPyで実装)
hsv = rgb_to_hsv(img)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/hsv/output2.png", hsv)