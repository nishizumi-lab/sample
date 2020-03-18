# -*- coding: utf-8 -*-
import cv2

def main():
    img = cv2.imread("test.jpg")  # 画像を読み込み
    cv2.imshow("Show",img)        # ウィンドウの表示
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
