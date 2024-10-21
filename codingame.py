from board import Board
from algo import Algo

class Codingame:
    def run(self):
        # my_id: 0 or 1 (Player 0 plays first)
        # opp_id: if your index is 0, this will be 1, and vice versa
        ids = input()
        board = Board()
        algo = Algo()

        # game loop
        while True:
            move_count = int(input())  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            if move_count <= 1:
                time_control = 0.95
            else:
                time_control = 0.095

            # Do not read the following lines
            for i in range(7):
                _ = input()  # one row of the board (from top to bottom)
            num_valid_actions = int(input())  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                _ = input()  # a valid column index into which a chip can be dropped

            opp_previous_action = int(input())  # opponent's previous chosen column index (will be -1 for first player in the first turn)
            if opp_previous_action == -2: # Opponent steal
                board = board.move(-1)
            elif opp_previous_action != -1:
                board = board.move(opp_previous_action)
            action = algo.next_move(board, time_control)
            board = board.move(action)

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)


            # Output a column index to drop the chip in. Append message to show in the viewer.
            if action == -1:
                print(-2)
            else:
                print(action)


if __name__ == '__main__':
    Codingame().run()
