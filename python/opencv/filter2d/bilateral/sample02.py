import cv2 as cv
import numpy as np

def update(val):
    # トラックバーの位置に基づいてパラメータを取得
    d = cv.getTrackbarPos('d', 'Bilateral Filter')
    sigmaColor = cv.getTrackbarPos('sigmaColor', 'Bilateral Filter')
    sigmaSpace = cv.getTrackbarPos('sigmaSpace', 'Bilateral Filter')

    # バイラテラルフィルタを適用
    filtered = cv.bilateralFilter(img, d, sigmaColor, sigmaSpace)

    # フィルタ処理後の画像を表示
    cv.imshow('Bilateral Filter', filtered)

# 入力画像を読み込む
img = cv.imread('C:/github/sample/python/opencv/filter2d/bilateral/input.jpg')

# ウィンドウを作成
cv.namedWindow('Bilateral Filter')

# トラックバーを作成
cv.createTrackbar('d', 'Bilateral Filter', 9, 50, update)
cv.createTrackbar('sigmaColor', 'Bilateral Filter', 75, 200, update)
cv.createTrackbar('sigmaSpace', 'Bilateral Filter', 75, 200, update)

# 初期表示
update(0)

# ユーザーが 'q' キーを押すまで待機
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
