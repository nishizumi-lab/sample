# -*- coding: utf-8 -*-
import cv2
import numpy as np


def template_matching_zncc(src, temp):
    # 画像の高さ・幅を取得
    h, w = src.shape
    ht, wt = temp.shape

    # スコア格納用の2次元リスト
    score = np.empty((h-ht, w-wt))

    # 配列のデータ型をuint8からfloatに変換
    src = np.array(src, dtype="float")
    temp = np.array(temp, dtype="float")

    # テンプレート画像の平均画素値
    mu_t = np.mean(temp)

    # 走査
    for dy in range(0, h - ht):
        for dx in range(0, w - wt):
            # 窓画像
            roi = src[dy:dy + ht, dx:dx + wt]
            # 窓画像の平均画素値
            mu_r = np.mean(roi)
            # 窓画像 - 窓画像の平均
            roi2 = roi - mu_r
            # テンプレート画像 - テンプレート画像の平均
            temp2 = temp - mu_t

            # ZNCCの計算式
            num = np.sum(roi2 * temp2)

            score[dy, dx] = num

    # スコアが最大(1に最も近い)の走査位置を返す
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
pt = template_matching_zncc(gray, temp)

# テンプレートマッチングの結果を出力
cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)

# 結果を出力
cv2.imwrite("D:/github/sample/python/opencv/template-matching/zncc2.png", img)
