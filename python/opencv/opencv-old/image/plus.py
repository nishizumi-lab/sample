# -*- coding: utf-8 -*-
import cv2

def main():
    # 2枚の画像をグレースケールで取得
    im1 = cv2.imread("test1.png",0)
    im2 = cv2.imread("test2.png",0)
    # 画像データを重ねあわせ
    im = im1 + im2
    cv2.imshow("test",im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()    # ウィンドウ破棄
    
if __name__ == '__main__':
    main()
