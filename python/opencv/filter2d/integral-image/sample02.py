# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np

def median_filter(src, ksize):
    # 畳み込み演算をしない領域の幅
    # width of skip
    d = int((ksize-1)/2)
    h, w = src.shape[:2]

    # 出力画像用の配列（要素は入力画像と同じ）
    dst = src.copy()

    for y in range(d, h - d):
        for x in range(d, w - d):
            for c in range(3):
                # 近傍にある画素値の中央値を出力画像の画素値に設定
                dst[y, x, c] = np.median(src[y-d:y+d+1, x-d:x+d+1, c])

    return dst

# 入力画像をカラーで読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.jpg")

# 処理時間の計測開始
start_time = time.time()

# メディアンフィルタの適用
dst = median_filter(img, ksize=5)

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output.jpg", dst)

# Processing Time: 16.600747 seconds