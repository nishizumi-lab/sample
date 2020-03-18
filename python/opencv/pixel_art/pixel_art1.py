# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 減色処理
def sub_color(src, K):
    # 次元数を1落とす
    Z = src.reshape((-1,3))

    # float32型に変換
    Z = np.float32(Z)

    # 基準の定義
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # K-means法で減色
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # UINT8に変換
    center = np.uint8(center)

    res = center[label.flatten()]

    # 配列の次元数と入力画像と同じに戻す
    return res.reshape((src.shape))


# モザイク処理
def mosaic(img, alpha):
    # 画像の高さ、幅、チャンネル数
    h, w, ch = img.shape

    # 縮小→拡大でモザイク加工
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)

    return img


# ドット絵化
def pixel_art(img, alpha=2, K=4):
    # モザイク処理
    img = mosaic(img, alpha)

    # 減色処理
    return sub_color(img, K)


# 入力画像を取得
img = cv2.imread("C:/github/sample/python/opencv/sample_data/input.png")

# ドット絵化
dst = pixel_art(img, 0.5, 4)
    
# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/pixel_art/dot1.png", dst)
