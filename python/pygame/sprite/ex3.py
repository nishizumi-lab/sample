# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN = Rect(0, 0, 400, 400)

# スプライトのクラス
class Sprite(pygame.sprite.Sprite):
    # スプライトを作成(画像ファイル名, 位置xy(x, y), 速さvxy(vx, vy), 回転angle)
    def __init__(self, filename, xy, vxy, angle=0):
        x, y = xy
        vx, vy = vxy
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        if angle != 0:
            self.img = pygame.transform.rotate(self.image, angle)
        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(x, y, w, h)
        self.vx = vx
        self.vy = vy
        self.angle = angle

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁と衝突時の処理(跳ね返り)
        if self.rect.left < 0 or self.rect.right > SCREEN.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCREEN.height:
            self.vy = -self.vy
        # 壁と衝突時の処理(壁を超えないように)
        self.rect = self.rect.clamp(SCREEN)

    def draw(self, screen):
        screen.blit(self.img, self.rect)

# メイン


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)

    # スプライトグループを作成
    group = pygame.sprite.RenderUpdates()
    Sprite.containers = group

    # スプライトを作成(画像ファイル名, 位置(x, y), 速さ(vx, vy), 回転angle)
    player = Sprite(
        "C:/github/sample/python/pygame/sprite/player.png", (200, 200), (2, 0), 0)
    enemy1 = Sprite(
        "C:/github/sample/python/pygame/sprite/enemy1.png", (200, 200), (0, 2), 0)
    enemy2 = Sprite(
        "C:/github/sample/python/pygame/sprite/enemy2.png", (200, 200), (2, 2), 10)
    clock = pygame.time.Clock()

    # 背景の作成と描画（背景は最初に1回だけ描画）
    bg = pygame.Surface(SCREEN.size)
    bg.fill((0, 20, 0))  # 画面の背景色
    screen.blit(bg, (0, 0))
    pygame.display.update()

    while (1):
        clock.tick(30)  # フレームレート(30fps)
        group.clear(screen, bg)

        # スプライトグループを更新(キャラクタ3体を一括して更新)
        group.update()

        # スプライトを更新
        dirty_rects = group.draw(screen)

        # updateにdirty rectを渡すとその部分だけ更新するので効率よい
        # 画面更新
        pygame.display.update(dirty_rects)

        # イベント処理
        for event in pygame.event.get():
            # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()

main()
