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
    label = cv2.connectedComponentsWithStats(gray)
    # ラベルの個数nと各ラベルの重心座標cogを取得
    n = label[0] - 1
    cog = np.delete(label[3], 0, 0)
    # 重心に赤円を描く
    for i in xrange(n):
        im = cv2.circle(im,(int(cog[i][0]),int(cog[i][1])), 10, (0,0,255), -1)
    # ウィンドウ表示
    cv2.imshow("CoG", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
