# -*- coding: utf-8 -*-
import cv2
import numpy as np
import ImageGrab

def main():

    while(1):
        im = ImageGrab.grab((90, 90, 400, 300)) # デスクトップの始点(0,0),横400, 縦300の矩形部分をキャプチャ
        im = np.asarray(im)                     # OpenCVで扱うためにNumpy配列に変換
        im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB) # BGR→RGB
        cv2.imshow("desktop", im)               # 画面表示
        if cv2.waitKey(1) > 0:                  # キー入力があれば終了
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
