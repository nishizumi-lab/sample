# -*- coding: utf-8 -*-
import cv2

def main():
    im = cv2.imread("test.jpg")                     # 画像の読み込み
    cv2.pyrMeanShiftFiltering(im, 2, 30, im, 1)     # MeanShiftで領域分割
    cv2.imshow("Show",im)                           # ウィンドウの表示
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
