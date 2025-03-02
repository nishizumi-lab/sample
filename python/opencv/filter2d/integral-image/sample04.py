# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import time

# 入力画像をカラーで読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.jpg")

# 処理時間の計測開始
start_time = time.time()

# 各チャネルに対してメディアンフィルタを適用
channels = cv.split(img)
filtered_channels = [cv.medianBlur(c, ksize=5) for c in channels]
dst = cv.merge(filtered_channels)

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output.jpg", dst)

# Processing Time: 0.013000 seconds