import pygame
import sys
import random
import math

# 定数の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
SIZE = 600
BOARD_SIZE = 12
GRID_SIZE = SIZE // BOARD_SIZE

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("オセロゲーム")

class Othello:
    def __init__(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        mid = BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = WHITE
        self.board[mid - 1][mid] = BLACK
        self.board[mid][mid - 1] = BLACK
        self.board[mid][mid] = WHITE
        self.turn = BLACK

    def draw_board(self):
        screen.fill(GREEN)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if self.board[x][y] is not None:
                    self.draw_stone(x, y, self.board[x][y])

    def draw_stone(self, x, y, color):
        pygame.draw.circle(screen, color, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 4)

    def is_valid_move(self, x, y):
        if self.board[x][y] is not None:
            return False
        opponent = WHITE if self.turn == BLACK else BLACK
        valid = False
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
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
        opponent = WHITE if self.turn == BLACK else BLACK
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            pieces_to_flip = []
            nx, ny = x + dx, y + dy
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
                pieces_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == self.turn:
                for px, py in pieces_to_flip:
                    self.board[px][py] = self.turn

    def has_valid_move(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.is_valid_move(x, y):
                    return True
        return False

    def game_end(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        if black_count > white_count:
            return "黒側の勝利"
        elif white_count > black_count:
            return "白側の勝利"
        else:
            return "引き分け"

    def next_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.turn
            self.flip_stones(x, y)
            self.turn = WHITE if self.turn == BLACK else BLACK

    def cpu_move(self):
        best_move = self.mcts()
        if best_move:
            self.next_move(best_move[0], best_move[1])

    def mcts(self):
        simulations = 1000
        best_move = None
        best_win_ratio = -1
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.is_valid_move(x, y):
                    wins = 0
                    for _ in range(simulations):
                        wins += self.simulate(x, y)
                    win_ratio = wins / simulations
                    if win_ratio > best_win_ratio:
                        best_win_ratio = win_ratio
                        best_move = (x, y)
        return best_move

    def simulate(self, x, y):
        board_copy = [row[:] for row in self.board]
        turn_copy = self.turn
        self.board[x][y] = turn_copy
        self.flip_stones(x, y)
        turn_copy = WHITE if turn_copy == BLACK else BLACK
        while self.has_valid_move():
            valid_moves = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.is_valid_move(i, j)]
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            self.board[move[0]][move[1]] = turn_copy
            self.flip_stones(move[0], move[1])
            turn_copy = WHITE if turn_copy == BLACK else BLACK
        result = self.game_end()
        self.board = board_copy
        return 1 if result == "白側の勝利" else 0

def main():
    game = Othello()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == BLACK:
                x, y = event.pos
                x //= GRID_SIZE
                y //= GRID_SIZE
                game.next_move(x, y)
                if game.turn == WHITE:
                    game.cpu_move()
        game.draw_board()
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
