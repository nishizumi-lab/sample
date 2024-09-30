# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *

# 画面サイズ 600×500
SCREEN_SIZE = (600, 500)

def main():
    # Pygameの初期化
    pygame.init()      
    
    # 画面設定（大きさ600*500）                             
    screen = pygame.display.set_mode(SCREEN_SIZE)
    
    # タイトルバーの設定（表示する文字を指定）
    pygame.display.set_caption("GAME")              

    while True:
        # 画面を緑色(#R=0, G=255, B=0)で塗りつぶし
        screen.fill((0,255,0))

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