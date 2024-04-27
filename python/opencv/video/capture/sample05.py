#-*- coding:utf-8 -*-
import cv2 as cv

# カメラのキャプチャ
cap = cv.VideoCapture(0)

# カメラのfps、サイズを変更
print(cap.set(cv.CAP_PROP_FPS, 60))
print(cap.set(cv.CAP_PROP_FRAME_WIDTH, 640))
print(cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480))

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # フレームを表示
    cv.imshow("Frame", frame)

    # qキーが押されたら途中終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()