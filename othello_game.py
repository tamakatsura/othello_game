import pygame
import sys
import os

# 初期化
pygame.init()

# 定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
CELL_SIZE = 80
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE * CELL_SIZE) // 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Othello")
clock = pygame.time.Clock()

# フォント設定
# デフォルトフォントを使用
default_font = pygame.font.SysFont(None, 36)

# 日本語テキスト描画関数
def draw_text(text, font, color, surface, x, y):
    if font == default_font:
        # 日本語テキストを英語に置き換え
        text = text.replace("黒", "Black").replace("白", "White")
        text = text.replace("現在のプレイヤー:", "Current Player:")
        text = text.replace("黒の勝ち!", "Black Wins!").replace("白の勝ち!", "White Wins!")
        text = text.replace("引き分け!", "Draw!")
        text = text.replace("Rキーでリスタート", "Press R to Restart")
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

class OthelloGame:
    def __init__(self):
        # ボード初期化 (0: 空, 1: 黒, 2: 白)
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # 初期配置
        self.board[3][3] = 2  # 白
        self.board[3][4] = 1  # 黒
        self.board[4][3] = 1  # 黒
        self.board[4][4] = 2  # 白
        
        # 黒のターンから開始
        self.current_player = 1
        self.game_over = False
        self.valid_moves = self.get_valid_moves()
        
    def get_opponent(self):
        return 2 if self.current_player == 1 else 1
    
    def is_valid_position(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    
    def get_valid_moves(self):
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 0 and self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def is_valid_move(self, row, col):
        if self.board[row][col] != 0:
            return False
        
        opponent = self.get_opponent()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if not self.is_valid_position(r, c) or self.board[r][c] != opponent:
                continue
                
            r += dr
            c += dc
            while self.is_valid_position(r, c):
                if self.board[r][c] == 0:
                    break
                if self.board[r][c] == self.current_player:
                    return True
                r += dr
                c += dc
                
        return False
    
    def make_move(self, row, col):
        if (row, col) not in self.valid_moves:
            return False
        
        self.board[row][col] = self.current_player
        opponent = self.get_opponent()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            flips = []
            r, c = row + dr, col + dc
            
            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                flips.append((r, c))
                r += dr
                c += dc
                
            if self.is_valid_position(r, c) and self.board[r][c] == self.current_player and flips:
                for flip_r, flip_c in flips:
                    self.board[flip_r][flip_c] = self.current_player
        
        # ターン交代
        self.current_player = opponent
        self.valid_moves = self.get_valid_moves()
        
        # 相手がパスの場合
        if not self.valid_moves:
            self.current_player = self.get_opponent()
            self.valid_moves = self.get_valid_moves()
            
            # ゲーム終了判定
            if not self.valid_moves:
                self.game_over = True
                
        return True
    
    def count_discs(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)
        return black_count, white_count
    
    def get_winner(self):
        black_count, white_count = self.count_discs()
        if black_count > white_count:
            return "黒の勝ち!"
        elif white_count > black_count:
            return "白の勝ち!"
        else:
            return "引き分け!"

def draw_board(game):
    # 背景
    screen.fill(DARK_GREEN)
    
    # ボード
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_OFFSET_X + col * CELL_SIZE
            y = BOARD_OFFSET_Y + row * CELL_SIZE
            
            # マス目
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # 石
            if game.board[row][col] == 1:  # 黒
                pygame.draw.circle(screen, BLACK, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif game.board[row][col] == 2:  # 白
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            
            # 有効な手の表示
            if (row, col) in game.valid_moves:
                pygame.draw.circle(screen, LIGHT_GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 10)
    
    # スコア表示
    black_count, white_count = game.count_discs()
    draw_text(f"黒: {black_count}", default_font, BLACK, screen, 50, 50)
    draw_text(f"白: {white_count}", default_font, WHITE, screen, 50, 100)
    
    # 現在のプレイヤー表示
    if not game.game_over:
        draw_text(f"現在のプレイヤー: {'黒' if game.current_player == 1 else '白'}", default_font, BLACK, screen, SCREEN_WIDTH - 300, 50)
    else:
        draw_text(game.get_winner(), default_font, BLACK, screen, SCREEN_WIDTH - 300, 50)
        draw_text("Rキーでリスタート", default_font, BLACK, screen, SCREEN_WIDTH - 300, 100)

def main():
    game = OthelloGame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = pygame.mouse.get_pos()
                
                # ボード上の位置に変換
                if (BOARD_OFFSET_X <= x < BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and
                    BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE):
                    col = (x - BOARD_OFFSET_X) // CELL_SIZE
                    row = (y - BOARD_OFFSET_Y) // CELL_SIZE
                    game.make_move(row, col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = OthelloGame()
        
        draw_board(game)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
