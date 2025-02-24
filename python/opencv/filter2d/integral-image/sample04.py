#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
import time


# 入力画像をグレースケールで読み込み
gray = cv.imread("C:/github/sample/python/opencv/filter2d/integral-image/input.png", 0)

# 処理時間の計測開始
start_time = time.time()

dst = cv.medianBlur(gray, ksize=5)

# 処理時間の計測終了
end_time = time.time()

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/integral-image/output.png", dst)

# Processing Time: 0.004002 seconds