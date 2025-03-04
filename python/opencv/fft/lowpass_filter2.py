# -*- coding: utf-8 -*-
import numpy as np
import cv2

def lowpass_filter(src, sigma=0.5):
    # 高速フーリエ変換(2次元)
    src = np.fft.fft2(src)

    # 画像サイズ
    height, width = src.shape

    # 画像の中心座標
    cy, cx =  int(height/2), int(width/2)

    # 第1象限と第3象限、第1象限と第4象限を入れ替え
    fsrc =  np.fft.fftshift(src)

    # 入力画像と同じサイズで値0の配列を生成
    fdst = np.zeros(src.shape, dtype=complex)

    # ガウス分布のマスクを生成
    y, x = np.ogrid[:height, :width]
    mask = np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * (sigma * min(height, width) / 2)**2))

    # ガウス分布でフィルタリング(高周波成分ほど値を小さくする)
    fdst = fsrc * mask

    # 第1象限と第3象限、第1象限と第4象限を入れ替え(元に戻す)
    fdst =  np.fft.fftshift(fdst)

    # 高速逆フーリエ変換
    dst = np.fft.ifft2(fdst)

    # 実部の値のみを取り出し、符号なし整数型に変換して返す
    return  np.uint8(dst.real)


def main():
    # ガウス分布のパラメータ（小さいほどフィルタの影響が強くなる)
    sigma = 0.3

    # 入力画像を読み込み
    img = cv2.imread("C:/github/sample/python/opencv/fft/sample.jpg")

    # RGB画像をRed, Green, Blueの1チャンネル画像に分割
    img_blue, img_green, img_red = cv2.split(img)

    # ローパスフィルタ処理
    himg_blue = lowpass_filter(img_blue, sigma)
    himg_green = lowpass_filter(img_green, sigma)
    himg_red = lowpass_filter(img_red, sigma)

    # RGB画像に戻す
    himg = cv2.merge((himg_blue, himg_green, himg_red))

    # 処理結果を出力
    cv2.imwrite("C:/github/sample/python/opencv/fft/lowpass_filter2.jpg", himg)

if __name__ == "__main__":
    main()