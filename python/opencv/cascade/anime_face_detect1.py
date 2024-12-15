# -*- coding: utf-8 -*-
import cv2

# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/cascade/mina.jpg")

# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier(
    "C:/github/sample/python/opencv/cascade/lbpcascade_animeface.xml")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# アニメ顔領域の探索
face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

# 顔領域を赤色の矩形で囲む
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y+h), (0, 0, 200), 5)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/cascade/output1.png", gray)
cv2.imwrite("C:/github/sample/python/opencv/cascade/output2.png", img)
