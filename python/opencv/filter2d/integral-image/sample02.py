# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np

def filter2d(src, kernel, fill_value=-1):
    # get kernel size
    # カーネルサイズ
    m, n = kernel.shape

    # width of skip
    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)

    # get width height of input image
    # 入力画像の高さと幅
    h, w = src.shape[0], src.shape[1]

    # ndarray of destination
    # 出力画像用の配列
    if fill_value == -1:
        dst = src.copy()
    elif fill_value == 0:
        dst = np.zeros((h, w))
    else:
        dst = np.zeros((h, w))
        dst.fill(fill_value)

    # Spatial filtering
    # 畳み込み演算
    for y in range(d, h - d):
        for x in range(d, w - d):
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1] * kernel)

    return dst

# 入力画像をカラーで読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.jpg")

# カーネル（縦方向の輪郭検出用）
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])


blue, green, red = cv.split(img)

# 処理時間の計測開始
start_time = time.time()

# チャンネル分割して、各チャンネルに平均値フィルタを適用し、結合
blue, green, red = cv.split(img)
dst = cv.merge((filter2d(blue, kernel), filter2d(green, kernel), filter2d(red, kernel)))

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output2.jpg", dst)

# Processing Time: 8.277997 seconds