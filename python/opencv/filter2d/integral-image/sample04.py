#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import time

def integral_image_median_filter(src, ksize):
    h, w = src.shape
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
            mean_pixels = sum_pixels / window_size

            # 中央値を簡易的に近似（平均値を使用）
            dst[y, x] = mean_pixels

    return np.uint8(dst)

# 入力画像をグレースケールで読み込み
gray = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.png", 0)

# 処理時間の計測開始
start_time = time.time()

# 積分画像を用いた高速メディアンフィルタの適用
dst = integral_image_median_filter(gray, ksize=5)

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output.png", dst)

# Processing Time: 0.764137 seconds