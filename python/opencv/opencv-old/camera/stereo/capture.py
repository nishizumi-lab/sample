# -*- coding: utf-8 -*-
import cv2

def main():
    # カメラのキャプチャ
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    while(1):
        im1 = cap1.read()[1]        # カメラ1のフレーム取得
        im2 = cap2.read()[1]        # カメラ2のフレーム取得
        cv2.imshow("Left",im1)
        cv2.imshow("Right",im2)
        # キーが押されたらループから抜ける
        if cv2.waitKey(10) > 0:
            cap1.release()
            cap2.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
