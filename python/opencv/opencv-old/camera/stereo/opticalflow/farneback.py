# -*- coding: utf-8 -*-
import cv2

def main():
    cap = cv2.VideoCapture(0)
    im1 = cap.read()[1]                                     # カメラからフレームの取得
    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)           # フレームのグレースケール変換
    # カメラ映像の取得
    while(1):
        im2 = cap.read()[1]                                 # カメラからフレームの取得
        gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)       # フレームのグレースケール変換
        flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        horz = cv2.normalize(flow[...,0], None, 0, 255, cv2.NORM_MINMAX)
        vert = cv2.normalize(flow[...,1], None, 0, 255, cv2.NORM_MINMAX)
        horz = horz.astype('uint8')
        vert = vert.astype('uint8')
        cv2.imshow('Horizontal Component', horz)            # 水平方向のオプティカルフロー表示
        cv2.imshow('Vertical Component', vert)              # 垂直方向のオプティカルフロー表示
        im1 = im2
        k = cv2.waitKey(10)
        # Escキーが押されたら終了
        if k>0:
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
