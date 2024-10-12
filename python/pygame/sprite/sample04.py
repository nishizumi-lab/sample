# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *

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
    def __init__(self, filepath, pos, vxy, angle=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filepath).convert_alpha()
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle)
        x, y = pos
        vx, vy = vxy
        w = self.image.get_width()
        h = self.image.get_height()
        self.rect = Rect(x, y, w, h)
        self.vx = vx
        self.vy = vy
        self.angle = angle

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        if self.rect.left < 0 or self.rect.right > SCREEN.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCREEN.height:
            self.vy = -self.vy
        self.rect = self.rect.clamp(SCREEN)

        # 他のスプライトとの衝突判定
        for sprite in self.containers:
            if sprite != self and self.rect.colliderect(sprite.rect):
                self.vx = -self.vx
                self.vy = -self.vy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    girl_group = pygame.sprite.RenderUpdates()
    Girl.containers = girl_group

    girl1 = Girl(GIRL1_IMG_PATH, (300, 200), (2, 0), 0)
    girl2 = Girl(GIRL2_IMG_PATH, (200, 200), (0, 2), -20)
    girl3 = Girl(GIRL3_IMG_PATH, (100, 200), (2, 3), 0)
    girl4 = Girl(GIRL4_IMG_PATH, (200, 100), (1, 2), 20)
    girl5 = Girl(GIRL5_IMG_PATH, (300, 300), (2, 1), 0)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)
        screen.fill((0, 60, 0))
        girl_group.update()
        dirty_rects = girl_group.draw(screen)
        pygame.display.update(dirty_rects)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()