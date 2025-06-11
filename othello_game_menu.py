import pygame
import sys
import random

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
GRAY = (128, 128, 128)

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Othello")
clock = pygame.time.Clock()

# フォント設定
title_font = pygame.font.SysFont(None, 72)
menu_font = pygame.font.SysFont(None, 48)
default_font = pygame.font.SysFont(None, 36)

# 日本語テキスト描画関数
def draw_text(text, font, color, surface, x, y):
    # 日本語テキストを英語に置き換え
    text_mapping = {
        "黒": "Black",
        "白": "White",
        "現在のプレイヤー:": "Current Player:",
        "黒の勝ち!": "Black Wins!",
        "白の勝ち!": "White Wins!",
        "引き分け!": "Draw!",
        "Rキーでリスタート": "Press R to Restart",
        "Mキーでメニューに戻る": "Press M for Menu",
        "オセロ": "Othello",
        "対人モード": "VS Player",
        "コンピュータ対戦": "VS Computer",
        "コンピュータ対戦 (初級)": "VS Computer (Easy)",
        "コンピュータ対戦 (中級)": "VS Computer (Medium)",
        "コンピュータ対戦 (上級)": "VS Computer (Hard)",
        "初級": "Easy",
        "中級": "Medium",
        "上級": "Hard",
        "終了": "Exit"
    }
    
    # テキスト置換
    for jp, en in text_mapping.items():
        text = text.replace(jp, en)
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
        # 日本語テキストを英語に置き換え
        self.display_text = text
        text_mapping = {
            "黒": "Black",
            "白": "White",
            "現在のプレイヤー:": "Current Player:",
            "黒の勝ち!": "Black Wins!",
            "白の勝ち!": "White Wins!",
            "引き分け!": "Draw!",
            "Rキーでリスタート": "Press R to Restart",
            "Mキーでメニューに戻る": "Press M for Menu",
            "オセロ": "Othello",
            "対人モード": "VS Player",
            "コンピュータ対戦": "VS Computer",
            "コンピュータ対戦 (初級)": "VS Computer (Easy)",
            "コンピュータ対戦 (中級)": "VS Computer (Medium)",
            "コンピュータ対戦 (上級)": "VS Computer (Hard)",
            "初級": "Easy",
            "中級": "Medium",
            "上級": "Hard",
            "終了": "Exit"
        }
        
        # テキスト置換
        for jp, en in text_mapping.items():
            self.display_text = self.display_text.replace(jp, en)
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_obj = self.font.render(self.display_text, True, BLACK)
        text_rect = text_obj.get_rect(center=self.rect.center)
        surface.blit(text_obj, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

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
        
        # ゲームモード (0: 対人, 1: コンピュータ)
        self.game_mode = 0
        # 難易度 (1: 初級, 2: 中級, 3: 上級)
        self.difficulty = 1
        
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
    
    # コンピュータの手を計算
    def get_computer_move(self):
        if not self.valid_moves:
            return None
        
        if self.difficulty == 1:  # 初級: ランダム
            return random.choice(self.valid_moves)
        
        elif self.difficulty == 2:  # 中級: 最も多く石を取れる手
            best_move = None
            max_flips = -1
            
            for move in self.valid_moves:
                row, col = move
                flips_count = self.count_flips(row, col)
                if flips_count > max_flips:
                    max_flips = flips_count
                    best_move = move
            
            return best_move
        
        elif self.difficulty == 3:  # 上級: 評価関数を使用
            best_move = None
            best_score = float('-inf')
            
            # 評価ボード (角と辺を高く評価)
            eval_board = [
                [100, -20, 10, 5, 5, 10, -20, 100],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [5, -2, -1, -1, -1, -1, -2, 5],
                [5, -2, -1, -1, -1, -1, -2, 5],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [100, -20, 10, 5, 5, 10, -20, 100]
            ]
            
            for move in self.valid_moves:
                row, col = move
                # 位置の評価値 + 裏返せる石の数
                score = eval_board[row][col] + self.count_flips(row, col) * 2
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_move
    
    # 指定した位置に石を置いた場合に裏返せる石の数を計算
    def count_flips(self, row, col):
        if self.board[row][col] != 0:
            return 0
        
        total_flips = 0
        opponent = self.get_opponent()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            flips = 0
            r, c = row + dr, col + dc
            
            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                flips += 1
                r += dr
                c += dc
                
            if self.is_valid_position(r, c) and self.board[r][c] == self.current_player and flips > 0:
                total_flips += flips
        
        return total_flips
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
        draw_text("Mキーでメニューに戻る", default_font, BLACK, screen, SCREEN_WIDTH - 300, 150)

def draw_menu():
    screen.fill(DARK_GREEN)
    
    # タイトル
    draw_text("オセロ", title_font, WHITE, screen, SCREEN_WIDTH // 2 - 100, 100)
    
    # メニューボタン
    buttons = []
    
    # 対人モード
    vs_player_btn = Button(SCREEN_WIDTH // 2 - 150, 250, 300, 60, "対人モード", menu_font, LIGHT_GREEN, GREEN)
    buttons.append(vs_player_btn)
    
    # コンピュータ対戦 (難易度別)
    vs_cpu_easy_btn = Button(SCREEN_WIDTH // 2 - 150, 330, 300, 60, "コンピュータ対戦 (初級)", menu_font, LIGHT_GREEN, GREEN)
    buttons.append(vs_cpu_easy_btn)
    
    vs_cpu_medium_btn = Button(SCREEN_WIDTH // 2 - 150, 410, 300, 60, "コンピュータ対戦 (中級)", menu_font, LIGHT_GREEN, GREEN)
    buttons.append(vs_cpu_medium_btn)
    
    vs_cpu_hard_btn = Button(SCREEN_WIDTH // 2 - 150, 490, 300, 60, "コンピュータ対戦 (上級)", menu_font, LIGHT_GREEN, GREEN)
    buttons.append(vs_cpu_hard_btn)
    
    # 終了ボタン
    exit_btn = Button(SCREEN_WIDTH // 2 - 150, 570, 300, 60, "終了", menu_font, LIGHT_GREEN, GREEN)
    buttons.append(exit_btn)
    
    # マウス位置取得
    mouse_pos = pygame.mouse.get_pos()
    
    # ボタン描画とホバー処理
    for button in buttons:
        button.check_hover(mouse_pos)
        button.draw(screen)
    
    return buttons

def game_loop():
    game = OthelloGame()
    menu_active = True
    running = True
    
    while running:
        if menu_active:
            # メニュー画面
            buttons = draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                mouse_pos = pygame.mouse.get_pos()
                
                # ボタンクリック処理
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 対人モード
                    if buttons[0].is_clicked(mouse_pos, event):
                        game = OthelloGame()
                        game.game_mode = 0  # 対人モード
                        menu_active = False
                    
                    # コンピュータ対戦 (初級)
                    elif buttons[1].is_clicked(mouse_pos, event):
                        game = OthelloGame()
                        game.game_mode = 1  # コンピュータ対戦
                        game.difficulty = 1  # 初級
                        menu_active = False
                    
                    # コンピュータ対戦 (中級)
                    elif buttons[2].is_clicked(mouse_pos, event):
                        game = OthelloGame()
                        game.game_mode = 1  # コンピュータ対戦
                        game.difficulty = 2  # 中級
                        menu_active = False
                    
                    # コンピュータ対戦 (上級)
                    elif buttons[3].is_clicked(mouse_pos, event):
                        game = OthelloGame()
                        game.game_mode = 1  # コンピュータ対戦
                        game.difficulty = 3  # 上級
                        menu_active = False
                    
                    # 終了
                    elif buttons[4].is_clicked(mouse_pos, event):
                        pygame.quit()
                        sys.exit()
        
        else:
            # ゲーム画面
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                    # プレイヤーの手番の場合のみクリック処理
                    if game.game_mode == 0 or (game.game_mode == 1 and game.current_player == 1):
                        x, y = pygame.mouse.get_pos()
                        
                        # ボード上の位置に変換
                        if (BOARD_OFFSET_X <= x < BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and
                            BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE):
                            col = (x - BOARD_OFFSET_X) // CELL_SIZE
                            row = (y - BOARD_OFFSET_Y) // CELL_SIZE
                            game.make_move(row, col)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and game.game_over:
                        # リスタート
                        game = OthelloGame()
                        game.game_mode = game.game_mode
                        game.difficulty = game.difficulty
                    elif event.key == pygame.K_m:
                        # メニューに戻る
                        menu_active = True
            
            # コンピュータの手番
            if game.game_mode == 1 and game.current_player == 2 and not game.game_over:
                # 少し遅延を入れる
                pygame.time.delay(500)
                computer_move = game.get_computer_move()
                if computer_move:
                    row, col = computer_move
                    game.make_move(row, col)
            
            draw_board(game)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
