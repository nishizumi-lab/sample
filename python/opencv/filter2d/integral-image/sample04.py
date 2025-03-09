# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import time

# 入力画像をカラーで読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.jpg")

# 処理時間の計測開始
start_time = time.time()

# 各チャネルに対してメディアンフィルタを適用
# チャンネル分割して、各チャンネルに積分画像を用いた平均値フィルタを適用し、結合
blue, green, red = cv.split(img)
dst = cv.merge((cv.medianBlur(blue, ksize=3), cv.medianBlur(green, ksize=3), cv.medianBlur(red, ksize=3)))

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output4.jpg", dst)

# Processing Time: 0.002890 seconds