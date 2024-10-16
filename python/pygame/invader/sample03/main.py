import pygame
import sys
import random

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 40, 0)

# 画像ファイルのパス
PLAYER_IMG_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/img/player.png"
ALIEN_IMG_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/img/alien.png"

# 音声ファイルのパス
SHOOT_SOUND_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/sound/shoot.mp3"
HIT_SOUND_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/sound/hit.mp3"
CLEAR_SOUND_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/sound/clear.mp3"
GAMEOVER_SOUND_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/sound/gameover.mp3"
GAMEPLAY_SOUND_PATH = "/Users/github/sample/python/pygame/invader/sample03/assets/sound/gameplay.mp3"

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
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
        self.image = pygame.image.load(ALIEN_IMG_PATH).convert_alpha()
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

# メインループ
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invaders")
    font = pygame.font.SysFont(None, 55)
    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    alien_bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    score = 0
    running = True
    game_over = False
    game_clear = False
    game_started = False
    gameplay_sound_played = False
    shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
    hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)
    clear_sound = pygame.mixer.Sound(CLEAR_SOUND_PATH)
    gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)
    gameplay_sound = pygame.mixer.Sound(GAMEPLAY_SOUND_PATH)
    
    shoot_sound.set_volume(0.2)
    hit_sound.set_volume(0.2)
    for i in range(10):
        for j in range(3):
            alien = Alien(50 + i * 50, 70 + j * 80, all_sprites, alien_bullets)
            all_sprites.add(alien)
            aliens.add(alien)

    while running:
        if not gameplay_sound_played and not game_over and not game_clear and game_started:
            gameplay_sound.play(-1)
            gameplay_sound_played = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    shoot_sound.play()
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_s:
                    game_started = True
                if game_over and event.key == pygame.K_r:
                    main()

        if not game_over and game_started:
            all_sprites.update()
            hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
            if hits:
                hit_sound.play()
                score += 10
            player_hits = pygame.sprite.spritecollide(player, alien_bullets, True)
            if player_hits:
                gameover_sound.play()
                game_over = True
            for alien in aliens:
                if alien.rect.bottom >= player.rect.top:
                    gameover_sound.play()
                    game_over = True
            if not aliens and not game_clear:
                clear_sound.play()
                game_clear = True

        screen.fill(DARK_GREEN)
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        if game_over:
            gameplay_sound.stop()
            game_over_text = font.render("GAME OVER - Press 'R' to Restart", True, WHITE)
            screen.blit(game_over_text, (150, 250))
            all_sprites.empty()
            aliens.empty()
            bullets.empty()
            alien_bullets.empty()
        if game_clear:
            gameplay_sound.stop()
            game_clear_text = font.render("GAME CLEAR", True, WHITE)
            screen.blit(game_clear_text, (300, 250))
            all_sprites.empty()
            aliens.empty()
            bullets.empty()
            alien_bullets.empty()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
