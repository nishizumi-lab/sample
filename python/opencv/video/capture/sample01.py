#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 動画ファイルのパス
filepath = "/Users/github/sample/python/opencv/video/input.mp4"

# 動画のキャプチャ
cap = cv2.VideoCapture(filepath)

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