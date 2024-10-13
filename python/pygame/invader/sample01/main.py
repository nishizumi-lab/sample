# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 40, 0)

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

# エイリアンクラス
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += 40

# 弾クラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

def main():
    # 初期化
    pygame.init()
    # 画面サイズ
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders")
    # フォントの設定
    font = pygame.font.SysFont(None, 55)
    # スプライトグループの作成
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        for j in range(3):
            alien = Alien(50 + i * 50, 70 + j * 80)
            all_sprites.add(alien)
            aliens.add(alien)
    # スコアの初期化
    score = 0
    # フラグ
    running = True
    game_over = False
    game_clear = False
    game_started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not game_clear:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_s:
                    game_started = True
                if event.key == pygame.K_r and game_over:
                    main()  # リスタート

        if not game_over and not game_clear and game_started:
            # 更新
            all_sprites.update()
            # 衝突判定
            hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
            if hits:
                score += 10
            # ゲームクリア判定
            if not aliens:
                game_clear = True
            # ゲームオーバー判定（エイリアンがプレイヤーの位置まで到達した場合）
            for alien in aliens:
                if alien.rect.bottom >= player.rect.top:
                    game_over = True
        # 描画
        screen.fill(DARK_GREEN)
        all_sprites.draw(screen)
        # スコア表示
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        # ゲームオーバー表示
        if game_over:
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (300, 250))
            restart_text = font.render("Press 'R' to Restart", True, WHITE)
            screen.blit(restart_text, (250, 300))
            # 古いスプライトグループの削除
            all_sprites.empty()
            aliens.empty()
            bullets.empty()

        # ゲームクリア表示
        if game_clear:
            game_clear_text = font.render("GAME CLEAR", True, WHITE)
            screen.blit(game_clear_text, (300, 250))

        # 画面更新
        pygame.display.flip()
        # フレームレート
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
