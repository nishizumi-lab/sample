# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import time

def mean_filter(src, ksize=5):
    h, w = src.shape[:2]
    d = ksize // 2
    dst = np.zeros_like(src, dtype=np.float32)


    # 積分画像を計算
    integral = cv.integral(src, sdepth=cv.CV_64F)

    for y in range(d, h - d):
        for x in range(d, w - d):
            # ウィンドウの境界を計算
            x1 = x - d
            x2 = x + d + 1
            y1 = y - d
            y2 = y + d + 1

            # ウィンドウ内のピクセル数
            window_size = (x2 - x1) * (y2 - y1)

            # 積分画像を使ってウィンドウ内のピクセルの合計を計算
            sum_pixels = integral[y2, x2] - integral[y1, x2] - integral[y2, x1] + integral[y1, x1]
            dst[y, x] = sum_pixels / window_size

    return np.uint8(dst)

# 入力画像をカラーで読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.jpg")

# 処理時間の計測開始
start_time = time.time()

# チャンネル分割して、各チャンネルに積分画像を用いた平均値フィルタを適用し、結合
blue, green, red = cv.split(img)
dst = cv.merge((mean_filter(blue), mean_filter(green), mean_filter(red)))

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output3.jpg", dst)

# Processing Time: 1.464988 seconds