# -*- coding:utf-8 -*-
import pygame
import sys
from pygame.locals import *

# 画面サイズ 600×500
SCREEN_SIZE = (600, 500)


def main():
    # Pygameの初期化
    pygame.init()

    # 画面設定（★起動時はフルスクリーン表示、解除時は指定したサイズ600*500になる）
    screen = pygame.display.set_mode(
        SCREEN_SIZE, FULLSCREEN)

    # タイトルバーに表示する文字
    pygame.display.set_caption("Test")

    while True:
        # 画面を黒色(#000000)に塗りつぶし
        screen.fill((0, 0, 0))

        # 画面を更新
        pygame.display.update()
        
        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT:  
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
    main()
