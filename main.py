from algo import Algo
from board import Board, State
from config import turn, width, time_control

def main():
    board = Board()
    algo = Algo()
    while board.winner == State.UNDETERMINED:
        print(board)
        if board.is_X_turn == turn:
            # human turn
            response = input("Your turn: ")
            while True:
                try:
                    response = int(response) - 1
                    if not board.is_valid_action(response):
                        response = input("Invalid move, try again: ")
                    else:
                        break
                except ValueError:
                    response = input("Not an integer, try again: ")
            
            board = board.move(response)
        
        else:
            # algo turn
            move = algo.next_move(board, time_control)
            if move == -1:
                print("Algo choose: steal")
            else:
                print(f"Algo choose: {move + 1}")
            board = board.move(move)
    
    print(board)
    if board.winner == State.DRAW:
        print("Draw!")
    else:
        is_X_win = board.winner == State.X
        if is_X_win == turn:
            print("You win!")
        else:
            print("Algo win!")

if __name__ == '__main__':
    main()
