# -*- coding: utf-8 -*-
import sys
import pygame
import numpy as np
from pygame.locals import *
import serial

def main():
    (w,h) = (400,400)   # 画面サイズ
    deg = 0             # 初期角度
    x = [0]*50          # 障害物のx座標
    y = [0]*50          # 障害物のy座標
    pygame.init()       # pygame初期化
    pygame.display.set_mode((w, h), 0, 32)  # 画面設定
    screen = pygame.display.get_surface()
    ser = serial.Serial("COM3")  # COMポート(Arduino接続)
    while (1):
        data = ser.readline().rstrip()  # \nまで読み込む(\nは削除)
        (deg, L) = data.split(",")
        (deg, L) = (int(deg), int(L))
        # レーダービームの軌跡描画
        for i in range(1, 50):
            dx = w/2 * np.cos(np.radians(deg-i)) + w/2
            dy = h/2 * np.sin(np.radians(deg-i)) + h/2
            pygame.draw.aaline(screen, (0, 235/i+20, 0), (w/2, h/2), (dx, dy),0)
        # レーダー画面の目盛描画
        pygame.draw.circle(screen, (0, 200, 0), (w/2, h/2), w/2, 1)
        pygame.draw.circle(screen, (0, 200, 0), (w/2, h/2), w/4, 1)
        pygame.draw.line(screen, (0, 200, 0), (0, h/2), (w, h/2))
        pygame.draw.line(screen, (0, 200, 0), (w/2, 0), (w/2, h))
        # 障害物の描画
        x0 = int(L*np.cos(np.radians(deg))) + w/2
        y0 = int(L*np.sin(np.radians(deg))) + h/2
        x.pop(49)
        y.pop(49)
        x.insert(0,x0)
        y.insert(0,y0)
        for i in range(1, len(x)):
            pygame.draw.circle(screen, (0, 255, 0), (x[i], y[i]), 3)
        pygame.display.update()         # 画面更新
        screen.fill((0, 20, 0, 0))      # 画面の背景色

        # イベント
        for event in pygame.event.get():
            if event.type == QUIT:      # 閉じるボタンが押されたら終了
                pygame.quit()           # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
        main()

