# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *


# 画面サイズ 600×500
SCREEN_SIZE = (600, 500)

def main():
    # Pygameの初期化
    pygame.init()  

    # 画面の生成
    screen = pygame.display.set_mode(SCREEN_SIZE)               
    pygame.display.set_caption("GAME")                          # タイトルバーに表示する文字

    while True:
        screen.fill((0,0,0))                                    # 画面を黒色に塗りつぶし

        # (0,0)から(80,80)まで線幅5pxで緑色(R=0, G=255, B=0)の直線を描く
        pygame.draw.line(screen, (0,255,0), (0,0), (80,80), 5)   # 直線の描画

        # 左上座標(10,10)、幅80px、高さ50pxの長方形を線幅5pxの赤色(R=255, G=0, B=0)で描く
        pygame.draw.rect(screen,(255,0,0),(100,100,180,150),5)   # 四角形を描画(塗りつぶしなし)
        #pygame.draw.rect(screen,(0,0,255),(10,10,80,50))    # 四角形を描画(塗りつぶし)

        # 左上の座標が(50,50)、幅が150、高さが50の矩形に内接する楕円を線幅5pxの緑色(R=0, G=100, B=0)で描く
        pygame.draw.ellipse(screen,(0,0,255),(250,250,300,200),5) # 円を描画(塗りつぶしなし)
        #pygame.draw.ellipse(screen,(0,0,255),(50,50,200,100))     # 円を描画(塗りつぶし)

        pygame.display.update()                                 # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:                              # 閉じるボタンが押されたら終了
                pygame.quit()                                   # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
    main()