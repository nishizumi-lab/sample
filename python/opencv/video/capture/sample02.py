#-*- coding:utf-8 -*-
import cv2 as cv


# カメラのキャプチャ
cap = cv.VideoCapture(0)

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # フレームを表示
    cv.imshow("Flame", frame)

    # qキーが押されたら途中終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()