# -*- coding: utf-8 -*-
import cv2

def main():
    im = cv2.imread("test.jpg") # 画像を読み込み
    im = cv2.flip(im,0)         # 上下反転
    cv2.imshow("Show",im)       # 画面表示
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
