# -*- coding: utf-8 -*-
import cv2
import numpy as np


def template_matching_sad(src, temp):
    # 画像の高さ・幅を取得
    h, w = src.shape
    ht, wt = temp.shape

    # スコア格納用の二次元配列
    score = np.empty((h-ht, w-wt))

    # 走査
    for dy in range(0, h - ht):
        for dx in range(0, w - wt):
            # 差分の絶対和を計算
            diff = np.abs(src[dy:dy + ht, dx:dx + wt] - temp)
            score[dy, dx] = diff.sum()

    # スコアが最小の走査位置を返す
    pt = np.unravel_index(score.argmin(), score.shape)

    return (pt[1], pt[0])


# 入力画像の読み込み
img = cv2.imread("D:/github/sample/python/opencv/template-matching/input.png")
temp = cv2.imread("D:/github/sample/python/opencv/template-matching/temp.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)

# テンプレート画像の高さ・幅
h, w = temp.shape

# テンプレートマッチング（NumPyで実装）
pt = template_matching_sad(gray, temp)

# テンプレートマッチングの結果を出力
cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)

# 結果を出力
cv2.imwrite("D:/github/sample/python/opencv/template-matching/sad2.png", img)
