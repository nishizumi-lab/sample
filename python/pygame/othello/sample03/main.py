import pygame
import sys
import random
import copy

# 定数の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
SIZE = 600
BOARD_SIZE = 8
GRID_SIZE = SIZE // BOARD_SIZE

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("オセロゲーム（ミニマックス法）")

class Othello:
    """オセロのゲームロジックと描画を管理するクラス。"""

    def __init__(self):
        """初期盤面とターンの設定を行う。"""
        # BOARD_SIZE x BOARD_SIZE の盤面を None（石なし）で初期化
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        mid = BOARD_SIZE // 2
        # 初期配置（中央に4つの石を交互に配置）
        self.board[mid - 1][mid - 1] = WHITE
        self.board[mid - 1][mid] = BLACK
        self.board[mid][mid - 1] = BLACK
        self.board[mid][mid] = WHITE
        # プレイヤーのターン（黒が先手）
        self.turn = BLACK

    def draw_board(self):
        """現在の盤面を画面に描画する。"""
        screen.fill(GREEN)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                # 升目の枠線を描画
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                # 石がある場合は描画
                if self.board[x][y] is not None:
                    self.draw_stone(x, y, self.board[x][y])

    def draw_stone(self, x, y, color):
        """指定された座標に石を描画する。

        Args:
            x (int): 盤面のx座標。
            y (int): 盤面のy座標。
            color (tuple): 石の色 (RGB)。
        """
        pygame.draw.circle(screen, color, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 4)

    def is_valid_move(self, x, y):
        """指定された座標に石が置けるかどうかを判定する。

        Args:
            x (int): 盤面のx座標。
            y (int): 盤面のy座標。

        Returns:
            bool: 置ける場合はTrue、そうでない場合はFalse。
        """
        # 既に石がある場所には置けない
        if self.board[x][y] is not None:
            return False
        
        opponent = WHITE if self.turn == BLACK else BLACK
        valid = False
        
        # 8方向（上下左右、斜め）をチェック
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            # 隣のマスが相手の色であることを確認
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
                # その方向にさらに進んで、自分の色で挟めるかを確認
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    nx += dx
                    ny += dy
                    if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
                        break
                    if self.board[nx][ny] is None:
                        break
                    if self.board[nx][ny] == self.turn:
                        valid = True
                        break
        return valid

    def flip_stones(self, x, y):
        """置かれた石によって挟まれた相手の石をひっくり返す。

        Args:
            x (int): 置いた石のx座標。
            y (int): 置いた石のy座標。
        """
        opponent = WHITE if self.turn == BLACK else BLACK
        # 8方向に対して処理を行う
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            pieces_to_flip = []
            nx, ny = x + dx, y + dy
            # 相手の石が続く限りリストに追加
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
                pieces_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            # 最後に自分の石で挟まれていれば、リスト内の石をすべて自分の色に変える
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == self.turn:
                for px, py in pieces_to_flip:
                    self.board[px][py] = self.turn

    def has_valid_move(self):
        """現在のプレイヤーに置ける場所があるかどうかを確認する。

        Returns:
            bool: 置ける場所がある場合はTrue、そうでない場合はFalse。
        """
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.is_valid_move(x, y):
                    return True
        return False

    def game_end(self):
        """ゲーム終了時の勝敗メッセージを取得する。

        Returns:
            str: 勝敗を示すメッセージ。
        """
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        if black_count > white_count:
            return "黒側の勝利"
        elif white_count > black_count:
            return "白側の勝利"
        else:
            return "引き分け"

    def next_move(self, x, y):
        """石を置き、ターンを交代する。

        Args:
            x (int): 盤面のx座標。
            y (int): 盤面のy座標。
        """
        if self.is_valid_move(x, y):
            self.board[x][y] = self.turn
            self.flip_stones(x, y)
            # ターンの交代
            self.turn = WHITE if self.turn == BLACK else BLACK

    def cpu_move(self):
        """CPU（Minimax法）による着手を行う。"""
        best_score = float('-inf')
        best_move = None
        
        # すべてのマスに対して探索を行う
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.is_valid_move(x, y):
                    # 盤面の状態を一時保存
                    board_backup = copy.deepcopy(self.board)
                    
                    # 試しに置いてみる
                    self.board[x][y] = WHITE
                    self.flip_stones(x, y)
                    
                    # 再帰的にMinimax法を実行
                    # depth: 1 (次の深さ), is_maximizing: False (次は相手の番なので最小化を目指す)
                    score = self.minimax(1, False)
                    
                    # 盤面を元に戻す
                    self.board = board_backup
                    
                    # 最も高いスコアの着手を選択
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        
        if best_move:
            self.next_move(best_move[0], best_move[1])

    def minimax(self, depth, is_maximizing):
        """Minimax法による盤面評価を行う。

        Minimax法は、自分は利益を最大化し、相手は自分の利益を最小化（相手の利益を最大化）
        するように行動するという前提に基づいたアルゴリズムです。

        Args:
            depth (int): 現在の探索の深さ。
            is_maximizing (bool): 最大化を目指すターン（自分のターン）かどうか。

        Returns:
            int: 評価値。
        """
        # 探索の限界深さに達したか、置ける場所がなくなった場合は現在の盤面を評価
        if depth == 3 or not self.has_valid_move():
            return self.evaluate_board()

        if is_maximizing:
            # 自分のターン：評価値を最大化する着手を選ぶ
            max_eval = float('-inf')
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    if self.is_valid_move(x, y):
                        board_backup = copy.deepcopy(self.board)
                        self.board[x][y] = WHITE
                        self.flip_stones(x, y)
                        
                        # 子ノードの評価値を取得（相手のターンになるので最小化）
                        eval = self.minimax(depth + 1, False)
                        
                        self.board = board_backup
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            # 相手のターン：評価値を最小化する（相手が最善を尽くす）と想定
            min_eval = float('inf')
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    if self.is_valid_move(x, y):
                        board_backup = copy.deepcopy(self.board)
                        self.board[x][y] = BLACK
                        self.flip_stones(x, y)
                        
                        # 子ノードの評価値を取得（自分のターンになるので最大化）
                        eval = self.minimax(depth + 1, True)
                        
                        self.board = board_backup
                        min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self):
        """盤面の有利不利を数値化する評価関数。

        Returns:
            int: CPU側（白）の優位性（白の数 - 黒の数）。
        """
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        # CPU（白）の石が多いほど高いスコアになるように計算
        return white_count - black_count

def main():
    """ゲームのメインループを管理する。"""
    game = Othello()
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # プレイヤー（黒）のクリック操作
            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == BLACK:
                x, y = event.pos
                x //= GRID_SIZE
                y //= GRID_SIZE
                game.next_move(x, y)
        
        # CPU（白）のターン
        if game.turn == WHITE:
            # パスが必要かチェック
            if not game.has_valid_move():
                game.turn = BLACK
            else:
                game.cpu_move()
        
        # プレイヤーがパスしなければならない場合
        if game.turn == BLACK and not game.has_valid_move():
            if not any(game.is_valid_move(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) for game.turn in [WHITE]):
                # 両者置けなくなったら終了
                print(game.game_end())
                break
            game.turn = WHITE

        # 描画更新
        game.draw_board()
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

