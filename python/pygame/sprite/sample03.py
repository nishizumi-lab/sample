# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

# 画面サイズ
SCREEN = Rect(0, 0, 600, 400)   # 画面サイズ

# 画像ファイルパス
GIRL1_IMG_PATH = "/Users/github/sample/python/pygame/sprite/girl1.png"
GIRL2_IMG_PATH = "/Users/github/sample/python/pygame/sprite/girl2.png"
GIRL3_IMG_PATH = "/Users/github/sample/python/pygame/sprite/girl3.png"
GIRL4_IMG_PATH = "/Users/github/sample/python/pygame/sprite/girl4.png"
GIRL5_IMG_PATH = "/Users/github/sample/python/pygame/sprite/girl5.png"

# スプライトのクラス
class Girl(pygame.sprite.Sprite):
    # スプライトの初期化(画像ファイル名, 位置pos(x, y), 速さvxy(vx, vy), 回転angle)
    def __init__(self, filepath, pos, vxy, angle=0):

        # デフォルトグループをセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filepath).convert_alpha()
        if angle != 0: 
            self.image = pygame.transform.rotate(self.image, angle)
        
        # 矩形オブジェクトの作成
        x, y = pos
        vx, vy = vxy
        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(x, y, w, h)

        # 移動速度、角度
        self.vx = vx
        self.vy = vy
        self.angle = angle
    
    # 更新
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁と衝突時の処理(跳ね返り)
        if self.rect.left < 0 or self.rect.right > SCREEN.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCREEN.height:
            self.vy = -self.vy
        # 壁と衝突時の処理(壁を超えないように)
        self.rect = self.rect.clamp(SCREEN)
    # 描画
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# メイン
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)

    # スプライトグループの作成
    group = pygame.sprite.RenderUpdates()

    # Girlクラスにスプライトグループを割り当てる
    Girl.containers = group
    
    # スプライトを作成(画像ファイル名, 位置(x, y), 速さ(vx, vy), 回転angle)
    girl1 = Girl(GIRL1_IMG_PATH,(200, 200), (2, 0), 0)
    girl2 = Girl(GIRL2_IMG_PATH,(200, 200), (0, 2), -20)
    girl3 = Girl(GIRL3_IMG_PATH,(200, 200), (2, 3), 0)
    girl4 = Girl(GIRL4_IMG_PATH,(200, 200), (1, 2), 20)
    girl5 = Girl(GIRL5_IMG_PATH,(200, 200), (2, 1), 0)

    clock = pygame.time.Clock()

    running = True  # ループ処理の実行を継続するフラグ

    while running:
        # フレームレート(30fps)
        clock.tick(30)

        # 画面の背景色
        screen.fill((0, 60, 0)) 

        # スプライトグループを更新
        group.update()

        # スプライトグループを描画
        dirty_rects = group.draw(screen)

        # 画面更新
        pygame.display.update(dirty_rects)

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT: 
                running = False
            # キーイベント
            if event.type == KEYDOWN:
                # Escキーが押されたら終了
                if event.key == K_ESCAPE:   
                    running = False
    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()