# -*- coding: utf-8 -*-
import cv2
import numpy as np

# モザイク処理
def mosaic(img, alpha):
    # 画像の高さと幅
    w = img.shape[1]
    h = img.shape[0]

    # 最近傍法で縮小→拡大することでモザイク加工
    img = cv2.resize(img, (int(w*alpha), int(h*alpha)))
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)

    return img


# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier(
    "C:/github/sample/python/opencv/cascade/haarcascade_frontalface_default.xml")

# 動画の読み込み
cap = cv2.VideoCapture("C:/github/sample/python/opencv/cascade/input.mp4")
#cap = cv2.VideoCapture(0) # webカメラ映像を扱う場合

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔領域の探索
    face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    # 顔領域を赤色の矩形で囲む
    for (x, y, w, h) in face:
        # 顔部分を切り出してモザイク処理
        frame[y:y+h, x:x+w] = mosaic(frame[y:y+h, x:x+w], 0.05)

    # フレームを表示
    cv2.imshow("Flame", frame)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
