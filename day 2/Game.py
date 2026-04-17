# Tic-Tac-Toe Game for two players

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    # Check rows, columns, diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]
        print(f"Player {current_player + 1}'s turn ({player})")

        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid position. Try again.")
                continue
            if board[row][col] != ' ':
                print("Position already taken. Try again.")
                continue

            board[row][col] = player

            if check_win(board, player):
                print_board(board)
                print(f"Player {current_player + 1} wins!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            current_player = 1 - current_player

        except ValueError:
            print("Invalid input. Please enter numbers.")

if __name__ == "__main__":
    main()