# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *

# 画面サイズ 600×500
SCREEN_SIZE = (600, 378)

# プレイヤーの画像ファイルパス
PLAYER_IMG_PATH = "/Users/github/sample/python/pygame/tutorial/player.png"

# 背景の画像ファイルパス
BACKGROUND_IMG_PATH = "/Users/github/sample/python/pygame/tutorial/background.png"

def main():
    # Pygameの初期化
    pygame.init()
    # 画面設定
    pygame.display.set_mode(SCREEN_SIZE)  
    screen = pygame.display.get_surface()

    # 背景画像の取得
    bg = pygame.image.load(BACKGROUND_IMG_PATH).convert_alpha()
    rect_bg = bg.get_rect()

    # プレイヤー画像の取得
    player = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
    rect_player = player.get_rect()

    # プレイヤー画像の初期位置
    rect_player.center = (330, 300) 

    while True:
        # 画面更新
        pygame.display.update()  
        # 更新間隔（30msec）           
        pygame.time.wait(30)
        # 画面の背景色（RGBA）     
        screen.fill((0, 0, 0, 0))
        # 背景画像の描画
        screen.blit(bg, rect_bg)
        # プレイヤー画像の描画    
        screen.blit(player, rect_player)   

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            # キーイベント
            if event.type == KEYDOWN:
                # Escキーが押されたら終了
                if event.key == K_ESCAPE:   
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
        main()
