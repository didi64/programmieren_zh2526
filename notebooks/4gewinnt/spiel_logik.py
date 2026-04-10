W = 7
H = 6


def neues_board():
    board = []
    for i in range(H):
        board.append([0] * W)
    return board


def spalte_voll(board, col):
    return board[0][col] != 0


def board_voll(board):
    for col in range(W):
        if board[0][col] == 0:
            return False
    return True


def stein_fallen_lassen(board, col, player):
    if spalte_voll(board, col):
        return -1

    row = H - 1
    while row >= 0 and board[row][col] != 0:
        row = row - 1

    board[row][col] = player
    return row


def check_win(board, player):
    for r in range(H):
        for c in range(W - 3):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    for c in range(W):
        for r in range(H - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    for r in range(H - 3):
        for c in range(W - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    for r in range(3, H):
        for c in range(W - 3):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

    return False


board = neues_board()