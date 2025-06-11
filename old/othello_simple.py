import pygame
import sys

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

# ゲーム状態
# 0: 空, 1: 黒, 2: 白
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 初期配置
board[3][3] = 2  # 白
board[3][4] = 1  # 黒
board[4][3] = 1  # 黒
board[4][4] = 2  # 白

# 現在のプレイヤー (1: 黒, 2: 白)
current_player = 1

# 画面設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

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
    global current_player
    current_player = 3 - current_player
    
    # 次のプレイヤーが置ける場所がない場合はスキップ
    if not get_valid_moves(current_player):
        print(f"Player {current_player} passes")
        current_player = 3 - current_player
        
        # 両方のプレイヤーが置けない場合はゲーム終了
        if not get_valid_moves(current_player):
            game_over()

def game_over():
    """ゲーム終了処理"""
    black_count, white_count = count_stones()
    print(f"Game Over! Black: {black_count}, White: {white_count}")
    
    if black_count > white_count:
        print("Black wins!")
    elif white_count > black_count:
        print("White wins!")
    else:
        print("Draw!")

# メインゲームループ
def main():
    global current_player
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # マウスクリック位置をボード座標に変換
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                
                # 有効な手であれば石を置く
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    if make_move(row, col, current_player):
                        print(f"Player {current_player} placed at ({row}, {col})")
                        switch_player()
        
        # 描画
        draw_board()
        
        # 石の数を表示
        black_count, white_count = count_stones()
        try:
            # 日本語フォントを使用
            font = pygame.font.Font(None, 30)  # デフォルトフォント
            # 日本語部分とそれ以外を分けて表示
            text_counts = font.render(f"Black: {black_count}  White: {white_count}  Turn: ", True, WHITE)
            text_player = font.render("Black" if current_player == 1 else "White", True, WHITE)
            screen.blit(text_counts, (10, 10))
            screen.blit(text_player, (text_counts.get_width() + 10, 10))
        except:
            # フォールバック: 英語で表示
            font = pygame.font.SysFont(None, 30)
            text = font.render(f"Black: {black_count}  White: {white_count}  Turn: {'Black' if current_player == 1 else 'White'}", True, WHITE)
            screen.blit(text, (10, 10))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
