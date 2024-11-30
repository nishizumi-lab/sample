# -*- coding: utf-8 -*-
import numpy as np
import cv2

def lowpass_filter(src, param = 0.5):
    # 高速フーリエ変換(2次元)
    src = np.fft.fft2(src)

    # 画像サイズ
    height, width = src.shape

    # 画像の中心座標
    cy, cx =  int(height/2), int(width/2)

    # フィルタのサイズ(矩形の高さと幅)
    rh, rw = int(param*cy), int(param*cx)

    # 第1象限と第3象限、第1象限と第4象限を入れ替え
    fsrc =  np.fft.fftshift(src)

    # 入力画像と同じサイズで値0の配列を生成
    fdst = np.zeros(src.shape, dtype=complex)

    # 中心部分の値だけ代入（中心部分以外は0のまま）
    fdst[cy-rh:cy+rh, cx-rw:cx+rw] = fsrc[cy-rh:cy+rh, cx-rw:cx+rw]

    # 第1象限と第3象限、第1象限と第4象限を入れ替え(元に戻す)
    fdst =  np.fft.fftshift(fdst)

    # 高速逆フーリエ変換
    dst = np.fft.ifft2(fdst)

    # 実部の値のみを取り出し、符号なし整数型に変換して返す
    return  np.uint8(dst.real)


def main():
    
    # フィルタのサイズ(倍率)、小さいほどフィルタの影響が強くなる
    param = 0.3

    # 入力画像を読み込み
    img = cv2.imread("C:/github/sample/python/opencv/fft/sample.jpg")

    # RGB画像をRed, Green, Blueの1チャンネル画像に分割
    img_blue, img_green, img_red = cv2.split(img)

    # ローパスフィルタ処理
    himg_blue = lowpass_filter(img_blue, param)
    himg_green = lowpass_filter(img_green, param)
    himg_red = lowpass_filter(img_red, param)

    # RGB画像に戻す
    himg = cv2.merge((himg_blue, himg_green, himg_red))

    # 処理結果を出力
    cv2.imwrite("C:/github/sample/python/opencv/fft/lowpass_filter.jpg", himg)

if __name__ == "__main__":
    main()