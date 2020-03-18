# -*- coding: utf-8 -*-
import cv2
import numpy as np

def main():
    # 入力画像の取得
    im = cv2.imread("test.jpg")
    # グレースケール変換
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 2値化
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # ラベリング処理
    n, label = cv2.connectedComponents(gray)
    # ラベルの個数nだけ色を用意
    rgbs = np.random.randint(0,255,(n+1,3))

    # ラベル付けした各マスクを色付け
    for y in xrange(0, gray.shape[0]):
        for x in xrange(0, gray.shape[1]):
            if label[y, x] > 0:
                im[y, x] = rgbs[label[y, x]]
            else:
                im[y, x] = [0, 0, 0]

    # ウィンドウ表示
    cv2.imshow("Labeling", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
