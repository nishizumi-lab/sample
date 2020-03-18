# -*- coding: utf-8 -*-
import cv2

def main():
    im = cv2.imread("test.jpg")                 # 画像の読み込み
    gray= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)   # 画像のグレースケール変換
    orb = cv2.ORB_create()                      # 検出器の初期化
    kp, des = orb.detectAndCompute(gray, None)  # 特徴量の検出と出力用の計算
    im = cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    # 特徴の描画
    cv2.imshow("Keypoint",im)                   # ウィンドウの表示
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
