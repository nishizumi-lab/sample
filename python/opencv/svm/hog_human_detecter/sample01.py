# -*- coding: utf-8 -*-
import cv2

# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/svm/hog_human_detecter/input.jpg")

# グレースケール変換（HOG計算用）
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# HOG特徴量 + SVMで人の識別器を作成
hog = cv2.HOGDescriptor()
    
# getDefaultPeopleDetector() を使用
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
# パラメータ設定
hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}

# 作成した識別器で人を検出
human, r = hog.detectMultiScale(gray, **hogParams)

# 人の領域を赤色の矩形で囲む
for (x, y, w, h) in human:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 200), 3)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/svm/hog_human_detecter/output.jpg", img)