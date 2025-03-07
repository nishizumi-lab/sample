#-*- coding:utf-8 -*-
import time
import cv2 as cv

# DoGフィルタ
def DoG(gray, ksize, sigma=1.1, k=1.1, threshold=10):
    # 標準偏差が異なる2つのガウシアン画像を算出
    gau1 = cv.GaussianBlur(gray, ksize, sigma)
    gau2 = cv.GaussianBlur(gray, ksize, k*sigma)

    # 2つのガウシアン画像の差分を出力
    dog = gau2 - gau1

    # 二値化処理
    _, binary = cv.threshold(dog, threshold, 255, cv.THRESH_BINARY)

    return binary

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/LoG/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 処理時間の計測開始
start_time = time.perf_counter()

# LoGフィルタの適用
dog_img = DoG(gray, (3,3), 1.0, 1.07, threshold=5)

# 処理時間の計測終了
end_time = time.perf_counter()

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoG/output.png', dog_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.001862 seconds