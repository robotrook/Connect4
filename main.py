# board and symbols used in board
game_board = []
x = "X"
o = "O"

# populates the game board as a blank board (.'s) are blank
for i in range(0, 6):
    game_board.append([])
    for j in range(0, 7):
        game_board[i].append('.')


# draws board
def draw_board(board):
    for i in range(0, 6):
        print("| ", end="")
        for j in range(0, 7):
            print(f'{board[i][j]} |', end=" ")
        print()
        print('------------------------------')
    print()

# adds a piece to board, pieces enter at the bottom of the board
def add_piece(board, side, column):
    for i in range(0, 6):
        if board[5-i][column] == ".":
            board[5-i][column] = side
            return 5-i


# checks slopes arranged like \
def downward_diagonal_win(board, x, y, depth):
    # is a chain of 4 possible from this position?
    if x + (3-depth) < 6 and y + (3-depth) < 5:
        if depth == 3:  # if this is the end of possible chain of, does it match the previous squares?
            if board[y][x] == board[y+1][x+1]:
                return True
            else:
                return False
    else:
        return False

# checks win conditions
def is_won(board):
    # vertical win, go through every possible vertical win
    for j in range(0, 7):
        for i in range(0, 3):
            if (board[i][j] != '.' and board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j]
            and board[i+2][j] == board[i + 3][j]):
                return board[i][j]

    # horizontal win, reverse of vertical win
    for i in range(0, 6):
        for j in range(0, 4):
            if(board[i][j] != '.' and board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2]
            and board[i][j+2] == board[i][j+3]):
                return board[i][j]

    # diagonal win /
    for i in range(0, 6):
        for j in range(0, 7):
            try:
                if (board[i][j] != "." and board[i][j] == board[i+1][j+1] and board[i+1][j+1] == board[i+2][j+2]
                and board[i+2][j+2] == board[i+3][j+3]):  # diagonal
                    return board[i][j]
            except IndexError:
                continue

    # diagonal win \
    for i in range(0, 6):
        for j in range(0, 7):
            try:
                if (board[i][j] != "." and board[i][j] == board[i-1][j+1] and board[i-1][j+1] == board[i-2][j+2]
                and board[i-2][j+2] == board[i-3][j+3]):  # anti diagonal
                    return board[i][j]
            except IndexError:
                continue

    # is a space empty?
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == ".":
                return None

    #  if none of these are true the game is a draw
    return "."

# minimax function for deciding which moves to play
def minimax(board, depth, is_max, alpha, beta):
    result = is_won(board)
    play_x = None

    # checks for win or for hitting the depth limit
    if depth == 8:
        return 50, None
    if result == x:
        return 50 - depth, None
    if result == o:
        return -50 + depth, None
    if result == ".":
        return 0, None

    # maximizer agent
    if is_max:
        # print("max called")
        best_val = -100  # worse than the worst possible value

        for j in range(0, 7):
            if board[0][j] == ".": # loops through all moves (inefficent?)
                r = add_piece(board, x, j) # r will be used to reset the board
                current_val, dummy = minimax(board, depth+1, False, alpha, beta)
                if current_val > best_val:
                    play_x = j
                    best_val = current_val

                board[r][j] = "."

                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break

        return best_val, play_x

    else:
        # print("min called")
        best_val = 100
        for j in range(0, 7):
            if board[0][j] == ".":
                r = add_piece(board, o, j)
                current_val, dummy = minimax(board, depth + 1, True, alpha, beta)
                if current_val < best_val:
                    play_x = j
                    best_val = current_val

                board[r][j] = "."

                beta = min(beta, best_val)
                if beta <= alpha:
                    break

        return best_val, play_x

#putting it all together
def game():
    global game_board, x, o
    while True:

        # check for win at start of x turn

        if is_won(game_board) == x:
            print("X won")
            break
        if is_won(game_board) == o:
            print("O won")
            break
        if is_won(game_board) == ".":
            print("draw!")
            break

        # X turn
        print("X thinking")
        eval, move = minimax(game_board, 0, True, -100, 100)
        print(f'played column {move+1}, eval is {eval}')
        add_piece(game_board, x, move)
        draw_board(game_board)

        # check for win at start of x turn
        if is_won(game_board) == x:
            print("X won")
            break
        if is_won(game_board) == o:
            print("O won")
            break
        if is_won(game_board) == ".":
            print("draw!")
            break

        # O turn
        print("O thinking")
        eval, move = minimax(game_board, 0, False, -100, 100)
        print(f'played column {move + 1}, eval is {eval}')
        add_piece(game_board, o, move)
        draw_board(game_board)


game()






