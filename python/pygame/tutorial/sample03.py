# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *

# 画面サイズ 600×500
SCREEN_SIZE = (600, 500)

def main():
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode(SCREEN_SIZE)  # 大きさ600*500の画面を生成
    pygame.display.set_caption("Test")  # タイトルバーに表示する文字

    while True:
        screen.fill((0, 0, 0))  # 画面を黒色(#000000)に塗りつぶし
        pygame.display.update()  # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()  # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
    main()
