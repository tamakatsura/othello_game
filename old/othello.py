import pygame
import sys
import random
import time

# 初期化
pygame.init()

# 定数
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
CELL_SIZE = WIDTH // BOARD_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# ゲームモード
MODE_MENU = 0
MODE_PVP = 1  # Player vs Player
MODE_PVC = 2  # Player vs Computer
MODE_GAME_OVER = 3

# 難易度
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

# グローバル変数
game_mode = MODE_MENU
difficulty = DIFFICULTY_MEDIUM
current_player = 1  # 1: 黒, 2: 白
player_color = 1    # プレイヤーの色 (コンピュータ対戦時)
board = None
game_over_message = ""

# 画面設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# フォント
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

def init_board():
    """ボードを初期化する"""
    global board, current_player
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # 初期配置
    board[3][3] = 2  # 白
    board[3][4] = 1  # 黒
    board[4][3] = 1  # 黒
    board[4][4] = 2  # 白
    
    current_player = 1  # 黒から開始

def draw_board():
    """ボードを描画する"""
    screen.fill(GREEN)
    
    # グリッド線を描画
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
    
    # 石を描画
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:  # 黒
                pygame.draw.circle(screen, BLACK, 
                                  (col * CELL_SIZE + CELL_SIZE // 2, 
                                   row * CELL_SIZE + CELL_SIZE // 2), 
                                  CELL_SIZE // 2 - 5)
            elif board[row][col] == 2:  # 白
                pygame.draw.circle(screen, WHITE, 
                                  (col * CELL_SIZE + CELL_SIZE // 2, 
                                   row * CELL_SIZE + CELL_SIZE // 2), 
                                  CELL_SIZE // 2 - 5)
    
    # 有効な手を表示
    valid_moves = get_valid_moves(current_player)
    for row, col in valid_moves:
        pygame.draw.circle(screen, GRAY, 
                          (col * CELL_SIZE + CELL_SIZE // 2, 
                           row * CELL_SIZE + CELL_SIZE // 2), 
                          CELL_SIZE // 8)
    
    # 石の数を表示
    black_count, white_count = count_stones()
    text_counts = font_small.render(f"Black: {black_count}  White: {white_count}  Turn: ", True, WHITE)
    text_player = font_small.render("Black" if current_player == 1 else "White", True, WHITE if current_player == 2 else WHITE)
    screen.blit(text_counts, (10, 10))
    screen.blit(text_player, (text_counts.get_width() + 10, 10))
    
    # メニューボタン
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH - 100, 10, 90, 30))
    menu_text = font_small.render("Menu", True, BLACK)
    screen.blit(menu_text, (WIDTH - 85, 15))

def draw_menu():
    """メニュー画面を描画する"""
    screen.fill(DARK_GREEN)
    
    # タイトル
    title = font_large.render("OTHELLO", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    
    # モード選択ボタン
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 150, 200, 300, 50))
    pvp_text = font_medium.render("Player vs Player", True, BLACK)
    screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, 210))
    
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 150, 280, 300, 50))
    pvc_text = font_medium.render("Player vs Computer", True, BLACK)
    screen.blit(pvc_text, (WIDTH // 2 - pvc_text.get_width() // 2, 290))
    
    # 難易度選択 (Player vs Computer モードのみ)
    difficulty_text = font_medium.render("Difficulty:", True, WHITE)
    screen.blit(difficulty_text, (WIDTH // 2 - 150, 360))
    
    # 難易度ボタン
    diff_width = 80
    diff_margin = 10
    diff_total_width = 3 * diff_width + 2 * diff_margin
    diff_start_x = WIDTH // 2 - diff_total_width // 2
    
    # Easy
    easy_color = RED if difficulty == DIFFICULTY_EASY else LIGHT_GRAY
    pygame.draw.rect(screen, easy_color, (diff_start_x, 400, diff_width, 40))
    easy_text = font_small.render("Easy", True, BLACK)
    screen.blit(easy_text, (diff_start_x + diff_width // 2 - easy_text.get_width() // 2, 410))
    
    # Medium
    medium_color = RED if difficulty == DIFFICULTY_MEDIUM else LIGHT_GRAY
    pygame.draw.rect(screen, medium_color, (diff_start_x + diff_width + diff_margin, 400, diff_width, 40))
    medium_text = font_small.render("Medium", True, BLACK)
    screen.blit(medium_text, (diff_start_x + diff_width + diff_margin + diff_width // 2 - medium_text.get_width() // 2, 410))
    
    # Hard
    hard_color = RED if difficulty == DIFFICULTY_HARD else LIGHT_GRAY
    pygame.draw.rect(screen, hard_color, (diff_start_x + 2 * (diff_width + diff_margin), 400, diff_width, 40))
    hard_text = font_small.render("Hard", True, BLACK)
    screen.blit(hard_text, (diff_start_x + 2 * (diff_width + diff_margin) + diff_width // 2 - hard_text.get_width() // 2, 410))
    
    # 色選択 (Player vs Computer モードのみ)
    color_text = font_medium.render("Play as:", True, WHITE)
    screen.blit(color_text, (WIDTH // 2 - 150, 460))
    
    # 色ボタン
    color_width = 120
    color_margin = 20
    color_total_width = 2 * color_width + color_margin
    color_start_x = WIDTH // 2 - color_total_width // 2
    
    # Black
    black_color = RED if player_color == 1 else LIGHT_GRAY
    pygame.draw.rect(screen, black_color, (color_start_x, 500, color_width, 40))
    black_text = font_small.render("Black", True, BLACK)
    screen.blit(black_text, (color_start_x + color_width // 2 - black_text.get_width() // 2, 510))
    
    # White
    white_color = RED if player_color == 2 else LIGHT_GRAY
    pygame.draw.rect(screen, white_color, (color_start_x + color_width + color_margin, 500, color_width, 40))
    white_text = font_small.render("White", True, BLACK)
    screen.blit(white_text, (color_start_x + color_width + color_margin + color_width // 2 - white_text.get_width() // 2, 510))

def draw_game_over():
    """ゲーム終了画面を描画する"""
    # 背景を半透明にする
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # ゲーム終了メッセージ
    game_over_text = font_large.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    
    # 勝者メッセージ
    result_text = font_medium.render(game_over_message, True, WHITE)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 20))
    
    # 石の数
    black_count, white_count = count_stones()
    score_text = font_medium.render(f"Black: {black_count}  White: {white_count}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 40))
    
    # メニューに戻るボタン
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50))
    menu_text = font_medium.render("Back to Menu", True, BLACK)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 110))

def get_directions():
    """8方向のベクトルを返す"""
    return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def is_valid_move(row, col, player):
    """指定された位置に石を置けるかチェック"""
    # すでに石がある場合は無効
    if board[row][col] != 0:
        return False
    
    opponent = 3 - player  # 相手のプレイヤー (1->2, 2->1)
    
    for dr, dc in get_directions():
        r, c = row + dr, col + dc
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) or board[r][c] != opponent:
            continue
        
        r += dr
        c += dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if board[r][c] == 0:
                break
            if board[r][c] == player:
                return True
            r += dr
            c += dc
    
    return False

def get_valid_moves(player):
    """プレイヤーが置ける場所のリストを返す"""
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col, player):
                valid_moves.append((row, col))
    return valid_moves

def count_flips(row, col, player):
    """指定位置に石を置いた場合にひっくり返せる石の数を返す"""
    if not is_valid_move(row, col, player):
        return 0
    
    opponent = 3 - player
    total_flips = 0
    
    for dr, dc in get_directions():
        flips = 0
        r, c = row + dr, col + dc
        
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
            flips += 1
            r += dr
            c += dc
        
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            total_flips += flips
    
    return total_flips

def make_move(row, col, player):
    """石を置き、挟まれた石をひっくり返す"""
    if not is_valid_move(row, col, player):
        return False
    
    board[row][col] = player
    opponent = 3 - player
    
    for dr, dc in get_directions():
        stones_to_flip = []
        r, c = row + dr, col + dc
        
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
            stones_to_flip.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            for flip_r, flip_c in stones_to_flip:
                board[flip_r][flip_c] = player
    
    return True

def count_stones():
    """黒と白の石の数を数える"""
    black_count = sum(row.count(1) for row in board)
    white_count = sum(row.count(2) for row in board)
    return black_count, white_count

def switch_player():
    """プレイヤーを交代する"""
    global current_player, game_mode
    current_player = 3 - current_player
    
    # 次のプレイヤーが置ける場所がない場合はスキップ
    if not get_valid_moves(current_player):
        print(f"Player {current_player} passes")
        current_player = 3 - current_player
        
        # 両方のプレイヤーが置けない場合はゲーム終了
        if not get_valid_moves(current_player):
            end_game()
            return
    
    # コンピュータの手番
    if game_mode == MODE_PVC and current_player != player_color:
        # 少し待ってからコンピュータの手を決定
        pygame.display.flip()
        time.sleep(0.5)
        computer_move()

def end_game():
    """ゲーム終了処理"""
    global game_mode, game_over_message
    
    black_count, white_count = count_stones()
    print(f"Game Over! Black: {black_count}, White: {white_count}")
    
    if black_count > white_count:
        game_over_message = "Black wins!"
    elif white_count > black_count:
        game_over_message = "White wins!"
    else:
        game_over_message = "Draw!"
    
    print(game_over_message)
    game_mode = MODE_GAME_OVER

def evaluate_board(player):
    """ボードの状態を評価する (コンピュータAI用)"""
    opponent = 3 - player
    
    # 石の数をカウント
    player_count = sum(row.count(player) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    
    # 角の位置をチェック (角は重要)
    corners = [(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]
    player_corners = sum(1 for r, c in corners if board[r][c] == player)
    opponent_corners = sum(1 for r, c in corners if board[r][c] == opponent)
    
    # 有効手の数をカウント (多いほど良い)
    player_moves = len(get_valid_moves(player))
    opponent_moves = len(get_valid_moves(opponent))
    
    # 評価値を計算
    # 難易度に応じて評価関数の重みを変える
    if difficulty == DIFFICULTY_EASY:
        # 簡単: 石の数だけを考慮
        score = player_count - opponent_count
    elif difficulty == DIFFICULTY_MEDIUM:
        # 中級: 石の数と角の位置を考慮
        score = (player_count - opponent_count) + 5 * (player_corners - opponent_corners)
    else:  # DIFFICULTY_HARD
        # 難しい: 石の数、角の位置、有効手の数を考慮
        score = (player_count - opponent_count) + 10 * (player_corners - opponent_corners) + 2 * (player_moves - opponent_moves)
    
    return score

def computer_move():
    """コンピュータの手を決定する"""
    global current_player
    
    valid_moves = get_valid_moves(current_player)
    if not valid_moves:
        return
    
    # 難易度に応じた手の選択
    if difficulty == DIFFICULTY_EASY:
        # 簡単: ランダムに選択
        row, col = random.choice(valid_moves)
    elif difficulty == DIFFICULTY_MEDIUM:
        # 中級: 最もひっくり返せる石が多い手を選択
        best_move = None
        max_flips = -1
        
        for r, c in valid_moves:
            flips = count_flips(r, c, current_player)
            if flips > max_flips:
                max_flips = flips
                best_move = (r, c)
        
        row, col = best_move
    else:  # DIFFICULTY_HARD
        # 難しい: ミニマックス法で最適な手を選択
        best_score = float('-inf')
        best_move = None
        
        for r, c in valid_moves:
            # 一時的に手を適用
            temp_board = [row[:] for row in board]
            make_move(r, c, current_player)
            
            # 評価
            score = evaluate_board(current_player)
            
            # 元に戻す
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    board[i][j] = temp_board[i][j]
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        row, col = best_move
    
    # 選択した手を適用
    make_move(row, col, current_player)
    print(f"Computer placed at ({row}, {col})")
    
    # プレイヤーに切り替え
    switch_player()

def handle_menu_click(pos):
    """メニュー画面でのクリックを処理する"""
    global game_mode, difficulty, player_color
    
    x, y = pos
    
    # Player vs Player ボタン
    if WIDTH // 2 - 150 <= x <= WIDTH // 2 + 150 and 200 <= y <= 250:
        game_mode = MODE_PVP
        init_board()
        return
    
    # Player vs Computer ボタン
    if WIDTH // 2 - 150 <= x <= WIDTH // 2 + 150 and 280 <= y <= 330:
        game_mode = MODE_PVC
        init_board()
        
        # コンピュータが先手の場合
        if player_color == 2:  # プレイヤーが白を選択
            computer_move()
        
        return
    
    # 難易度ボタン
    diff_width = 80
    diff_margin = 10
    diff_total_width = 3 * diff_width + 2 * diff_margin
    diff_start_x = WIDTH // 2 - diff_total_width // 2
    
    if 400 <= y <= 440:
        # Easy
        if diff_start_x <= x <= diff_start_x + diff_width:
            difficulty = DIFFICULTY_EASY
        # Medium
        elif diff_start_x + diff_width + diff_margin <= x <= diff_start_x + 2 * diff_width + diff_margin:
            difficulty = DIFFICULTY_MEDIUM
        # Hard
        elif diff_start_x + 2 * (diff_width + diff_margin) <= x <= diff_start_x + 3 * diff_width + 2 * diff_margin:
            difficulty = DIFFICULTY_HARD
    
    # 色選択ボタン
    color_width = 120
    color_margin = 20
    color_total_width = 2 * color_width + color_margin
    color_start_x = WIDTH // 2 - color_total_width // 2
    
    if 500 <= y <= 540:
        # Black
        if color_start_x <= x <= color_start_x + color_width:
            player_color = 1
        # White
        elif color_start_x + color_width + color_margin <= x <= color_start_x + 2 * color_width + color_margin:
            player_color = 2

def handle_game_click(pos):
    """ゲーム画面でのクリックを処理する"""
    global game_mode
    
    x, y = pos
    
    # メニューボタン
    if WIDTH - 100 <= x <= WIDTH - 10 and 10 <= y <= 40:
        game_mode = MODE_MENU
        return
    
    # ボード上のクリック
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        # プレイヤーの手番かつ有効な手の場合
        if (game_mode == MODE_PVP or (game_mode == MODE_PVC and current_player == player_color)):
            if make_move(row, col, current_player):
                print(f"Player {current_player} placed at ({row}, {col})")
                switch_player()

def handle_game_over_click(pos):
    """ゲーム終了画面でのクリックを処理する"""
    global game_mode
    
    x, y = pos
    
    # メニューに戻るボタン
    if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 150:
        game_mode = MODE_MENU

def main():
    """メインゲームループ"""
    global game_mode
    
    init_board()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if game_mode == MODE_MENU:
                    handle_menu_click(pos)
                elif game_mode == MODE_PVP or game_mode == MODE_PVC:
                    handle_game_click(pos)
                elif game_mode == MODE_GAME_OVER:
                    handle_game_over_click(pos)
        
        # 描画
        if game_mode == MODE_MENU:
            draw_menu()
        elif game_mode == MODE_PVP or game_mode == MODE_PVC:
            draw_board()
        elif game_mode == MODE_GAME_OVER:
            draw_board()
            draw_game_over()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
