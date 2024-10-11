# -*- coding: utf-8 -*-
import pygame
import sys

# 画面サイズ
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

# 音声ファイルパス
MUSIC_FILE_PATH = "/Users/github/sample/python/pygame/tutorial/sample.mp3"

def create_button(screen, text, x, y, width, height, color, action=None):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def main():
    pygame.init()
    pygame.mixer.init()
    
    # 画面設定
    screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
    pygame.display.set_caption("Music Player")
    
    # 音楽ファイルの読み込み
    pygame.mixer.music.load(MUSIC_FILE_PATH)
    
    # メインループ
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # ボタンの作成
        play_button = create_button(screen, "Play", 50, 200, 100, 50, (0, 180, 0))
        stop_button = create_button(screen, "Stop", 250, 200, 100, 50, (200, 0, 0))
        pause_button = create_button(screen, "Pause", 50, 100, 100, 50, (0, 0, 180))
        unpause_button = create_button(screen, "Unpause", 250, 100, 100, 50, (0, 0, 180))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    pygame.mixer.music.play(-1)
                if stop_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                if pause_button.collidepoint(event.pos):
                    pygame.mixer.music.pause()
                if unpause_button.collidepoint(event.pos):
                    pygame.mixer.music.unpause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()