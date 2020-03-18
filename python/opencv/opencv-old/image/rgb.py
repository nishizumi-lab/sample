# -*- coding: utf-8 -*-
import cv2

def main():
    im = cv2.imread("test.jpg",0)               # 画像をグレースケールで読み込み
    im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)   # グレースケール画像をRGB色空間に変換
    cv2.imshow("Show",im)                       # ウィンドウの表示
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
