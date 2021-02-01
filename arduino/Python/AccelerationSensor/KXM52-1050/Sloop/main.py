# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import serial
import sys

def main():
    ser = serial.Serial("COM7")  # COMポート(Arduino接続)
    xdegs = [0]*100              # 温度格納
    ydegs = [0]*100              # 温度格納
    t = np.arange(0,100,1)
    plt.ion()
    # Pygameの設定
    pygame.init()                                  # 初期化
    screen = pygame.display.set_mode((200, 200))   # 画面作成(100×100)
    pygame.display.set_caption("傾斜角度")         # タイトルバー
    font = pygame.font.Font(None, 30)              # 文字の設定

    while True:

        data = ser.readline().rstrip()  # \nまで読み込む(\nは削除)
        (xdeg, ydeg) = data.split(",")
        # 温度データのリスト更新
        xdegs.pop(99)
        xdegs.insert(0,float(xdeg))
        ydegs.pop(99)
        ydegs.insert(0,float(ydeg))
        # グラフ表示設定
        line, = plt.plot(t, xdegs, 'r-',label="X-axis[deg]") # Y軸更新
        line, = plt.plot(t, ydegs, 'b-',label="Y-axis[deg]") # Y軸更新
        line.set_ydata(xdegs)
        line.set_ydata(ydegs)
        plt.title("Real-time inclination angle")
        plt.xlabel("Time [s]")
        plt.ylabel("Inclination angle [deg]")
        plt.legend();plt.grid()
        plt.xlim([1,100]); plt.ylim([-90,90])
        plt.draw(); plt.clf()
        # Pygameの処理
        screen.fill((0,0,0))            # 画面のクリア
        text = font.render("(X, Y) = ("+xdeg+", "+ydeg+")", False, (255,255,255))
        screen.blit(text, (10, 10))     # レンダ，表示位置
        pygame.display.flip()           # 画面を更新して、変更を反映
        # Pygameのイベント処理
        for event in pygame.event.get():
            # 終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                ser.close()
                plt.close()
                sys.exit()


if __name__ == '__main__':
    main()
