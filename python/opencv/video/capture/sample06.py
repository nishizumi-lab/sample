#-*- coding:utf-8 -*-
import cv2
import numpy as np

filepath = "/Users/github/sample/python/opencv/video/input.mp4"

# 動画の読み込み
cap = cv2.VideoCapture(filepath)

# 200フレーム目から取得
cap.set(cv2.CAP_PROP_POS_FRAMES, 200)

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # フレームを表示
    cv2.imshow("Frame", frame)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()