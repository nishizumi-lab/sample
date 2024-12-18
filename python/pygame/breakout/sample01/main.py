# -*- coding: utf-8 -*-
import math
import sys
import pygame
from pygame.locals import *
import pygame.mixer

# 画面サイズ
SCREEN = Rect(0, 0, 400, 400)

# 画像ファイルのパス
PADDLE_IMG_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/img/paddle.png"
BLOCK_IMG_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/img/block.png"
BALL_IMG_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/img/ball.png"

# 音声ファイルのパス
PADDLE_SOUND_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/mp3/paddle_sound.mp3"
BLOCK_SOUND_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/mp3/block_sound.mp3"
GAMEOVER_SOUND_PATH = "/Users/github/sample/python/pygame/breakout/sample01/assets/mp3/gameover_sound.mp3"

# バドルのスプライトクラス
class Paddle(pygame.sprite.Sprite):
    # コンストラクタ（初期化メソッド）
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom - 20          # パドルのy座標

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]  # マウスのx座標をパドルのx座標に
        self.rect.clamp_ip(SCREEN)                     # ゲーム画面内のみで移動

# ボールのスプライトクラス
class Ball(pygame.sprite.Sprite):
    # コンストラクタ（初期化メソッド）
    def __init__(self, filename, paddle, blocks, score, speed, angle_left, angle_right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.dx = self.dy = 0  # ボールの速度
        self.paddle = paddle  # パドルへの参照
        self.blocks = blocks  # ブロックグループへの参照
        self.update = self.start # ゲーム開始状態に更新
        self.score = score
        self.hit = 0  # 連続でブロックを壊した回数
        self.speed = speed # ボールの初期速度
        self.angle_left = angle_left # パドルの反射方向(左端:135度）
        self.angle_right = angle_right # パドルの反射方向(右端:45度）

    # ゲーム開始状態（マウスを左クリック時するとボール射出）
    def start(self):
        # ボールの初期位置(パドルの上)
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

        # 左クリックでボール射出
        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move

    # ボールの挙動
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        # 壁との反射
        if self.rect.left < SCREEN.left:    # 左側
            self.rect.left = SCREEN.left
            self.dx = -self.dx              # 速度を反転
        if self.rect.right > SCREEN.right:  # 右側
            self.rect.right = SCREEN.right
            self.dx = -self.dx
        if self.rect.top < SCREEN.top:      # 上側
            self.rect.top = SCREEN.top
            self.dy = -self.dy

        # パドルとの反射(左端:135度方向, 右端:45度方向, それ以外:線形補間)
        # 2つのspriteが接触しているかどうかの判定
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.hit = 0                                # 連続ヒットを0に戻す
            (x1, y1) = (self.paddle.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.paddle.rect.right, self.angle_right)
            x = self.rect.left                          # ボールが当たった位置
            y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1  # 線形補間
            angle = math.radians(y)                     # 反射角度
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)
            self.paddle_sound.play()                    # 反射音

        # ボールを落とした場合
        if self.rect.top > SCREEN.bottom:
            self.update = self.start                    # ボールを初期状態に
            self.gameover_sound.play()
            self.hit = 0
            self.score.set_score(0)                               # スコアを0点にする
            #self.score.add_score(-100)                  # スコア減点-100点

        # ボールと衝突したブロックリストを取得（Groupが格納しているSprite中から、指定したSpriteと接触しているものを探索）
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:  # 衝突ブロックがある場合
            oldrect = self.rect
            for block in blocks_collided:
                # ボールが左からブロックへ衝突した場合
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                    
                # ボールが右からブロックへ衝突した場合
                if block.rect.left < oldrect.left and block.rect.right < oldrect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx

                # ボールが上からブロックへ衝突した場合
                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy

                # ボールが下からブロックへ衝突した場合
                if block.rect.top < oldrect.top and block.rect.bottom < oldrect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy
                self.block_sound.play()     # 効果音を鳴らす
                self.hit += 1               # 衝突回数をカウント
                self.score.add_score(self.hit * 10)   # 衝突回数に応じてスコア加点

# ブロック
class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        # ブロックの左上座標
        self.rect.left = SCREEN.left + x * self.rect.width
        self.rect.top = SCREEN.top + y * self.rect.height

# スコア
class Score():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 20)
        self.score = 0
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render("SCORE:" + str(self.score), True, (255,255,250))
        screen.blit(img, (self.x, self.y))
    def add_score(self, x):
        self.score += x
    def set_score(self, score):
        self.score = score

def main():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    Ball.paddle_sound = pygame.mixer.Sound(PADDLE_SOUND_PATH)    # パドルにボールが衝突した時の効果音取得
    Ball.block_sound = pygame.mixer.Sound(BLOCK_SOUND_PATH)    # ブロックにボールが衝突した時の効果音取得
    Ball.gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)    # ゲームオーバー時の効果音取得
    # 描画用のスプライトグループ
    group = pygame.sprite.RenderUpdates()  

    # 衝突判定用のスプライトグループ
    blocks = pygame.sprite.Group()   

    # スプライトグループに追加    
    Paddle.containers = group
    Ball.containers = group
    Block.containers = group, blocks

    # パドルの作成
    paddle = Paddle(PADDLE_IMG_PATH)

    # ブロックの作成(14*10)
    for x in range(1, 15):
        for y in range(1, 11):
            Block(BLOCK_IMG_PATH, x, y)

    # スコアを画面(10, 10)に表示
    score = Score(10, 10)    

    # ボールを作成
    Ball(BALL_IMG_PATH, paddle, blocks, score, 5, 135, 45)
    
    clock = pygame.time.Clock()

    running = True  # ループ処理の実行を継続するフラグ

    while running:
        clock.tick(60)      # フレームレート(60fps)
        screen.fill((0,20,0))
        # 全てのスプライトグループを更新
        group.update()
        # 全てのスプライトグループを描画       
        group.draw(screen)
        # スコアを描画  
        score.draw(screen) 
        # 画面更新 
        pygame.display.update()

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
