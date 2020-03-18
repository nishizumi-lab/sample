# -*- coding: utf-8 -*-
import cv2
import numpy as np


def anime_filter(img, K=20):
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # ぼかしでノイズ低減
    edge = cv2.blur(gray, (3, 3))

    # Cannyアルゴリズムで輪郭抽出
    edge = cv2.Canny(edge, 50, 150, apertureSize=3)

    # 輪郭画像をRGB色空間に変換
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 画像の減色処理
    img = np.array(img/K, dtype=np.uint8)
    img = np.array(img*K, dtype=np.uint8)

    # 差分を返す
    return cv2.subtract(img, edge)


def main():
    # 入力画像の読み込み
    img = cv2.imread("C:/github/sample/python/opencv/sample_data/input2.jpg")

    # 画像のアニメ絵化
    anime = anime_filter(img, 30)

    # 結果出力
    cv2.imwrite("C:/github/sample/python/opencv/anime_picture/anime.jpg", anime)


if __name__ == '__main__':
    main()
