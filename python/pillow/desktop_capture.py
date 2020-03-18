# -*- coding: utf-8 -*-
import ImageGrab

def main():
    im = ImageGrab.grab((0, 0, 400, 300))   # デスクトップの始点(0,0),横400, 縦300の矩形部分をキャプチャ
    im.save("desktop.png")                  # キャプチャした部分を画像ファイルに保存

if __name__ == "__main__":
    main()
