# -*- coding: utf-8 -*-
import sys
import pygame

# 画面サイズ
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 378

# 音声ファイルパス
MUSIC_FILE_PATH = "/Users/github/sample/python/pygame/tutorial/sample.mp3"

def main():
    # Pygameの初期化
    pygame.init()
    pygame.mixer.init()

    # 画面設定
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    screen = pygame.display.get_surface()

    # 音楽ファイルの読み込み
    pygame.mixer.music.load(MUSIC_FILE_PATH)

    # 音楽の再生
    pygame.mixer.music.play(-1)  # 無限ループで再生

    # メインループ
    running = True
    while running:
        # 画面更新
        pygame.display.update()  
        # 更新間隔（30msec）           
        pygame.time.wait(30)
        # 画面の背景色（RGBA）     
        screen.fill((0, 0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    # 終了処理
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
