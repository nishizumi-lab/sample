import pygame
import sys
import random

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
    def __init__(self, x, y, all_sprites, alien_bullets):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.all_sprites = all_sprites
        self.alien_bullets = alien_bullets

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += 40
        if random.randint(1, 300) == 1:  # 1/300の確率で弾を発射
            bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
            self.all_sprites.add(bullet)
            self.alien_bullets.add(bullet)

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

# エイリアンの弾クラス
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# リスタート関数
def restart_game():
    global all_sprites, aliens, bullets, alien_bullets, player, score, game_over, game_clear, game_started
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    alien_bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(10):
        for j in range(3):
            alien = Alien(50 + i * 50, 70 + j * 80, all_sprites, alien_bullets)
            all_sprites.add(alien)
            aliens.add(alien)

    score = 0
    game_over = False
    game_started = False
    game_clear = False

# メインループ
def main():
    global all_sprites, aliens, bullets, alien_bullets, player, score, game_over, game_clear, game_started
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders")
    font = pygame.font.SysFont(None, 55)

    restart_game()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_s:
                    game_started = True
                if game_over and event.key == pygame.K_r:
                    restart_game()

        if not game_over and game_started:
            all_sprites.update()

            hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
            if hits:
                score += 10

            # エイリアンの弾がプレイヤーに当たるとゲームオーバー
            player_hits = pygame.sprite.spritecollide(player, alien_bullets, True)
            if player_hits:
                game_over = True
            # ゲームオーバー判定（エイリアンがプレイヤーの位置まで到達した場合）
            for alien in aliens:
                if alien.rect.bottom >= player.rect.top:
                    game_over = True
            if not aliens:
                game_clear = True

        screen.fill(DARK_GREEN)
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("GAME OVER - Press 'R' to Restart", True, WHITE)
            screen.blit(game_over_text, (150, 250))

        # ゲームクリア表示
        if game_clear:
            game_clear_text = font.render("GAME CLEAR", True, WHITE)
            screen.blit(game_clear_text, (300, 250))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
