from typing import Literal, List, Tuple

from config import height, width, connect

class State:
    UNDETERMINED = 0
    X = 1
    O = 2
    DRAW = 3

class Board:
    def __init__(self, is_X_turn: bool=True,
                 X_table: Tuple[Tuple[bool, ...], ...]=None, O_table: Tuple[Tuple[bool, ...], ...]=None):
        """Instantiates a new table.
        Either:
        1. Both `X_table` and `O_table` are left blank, or
        2. Both `X_table` and `O_table` are provided with the correct dimension.
        """
        if X_table and O_table:
            self.X_table = X_table
            self.O_table = O_table
        else:
            self.X_table = tuple(tuple(False for _ in range(width)) for _ in range(height))
            self.O_table = tuple(tuple(False for _ in range(width)) for _ in range(height))
        self.is_X_turn = is_X_turn
        self._determine_winner()
    
    def actions(self) -> List[int]:
        """Returns the set of possible actions in this state.
        Each action is an int indicating the column to move at.
        """
        actions: List[int] = []
        for col in range(width):
            if self._is_column_movable(col):
                actions.append(col)
        return actions

    def _is_column_movable(self, col: int) -> bool:
        """Determines if a piece can be added at the column.
        """
        for row in range(height):
            if not self.X_table[row][col] and not self.O_table[row][col]:
                return True
        return False
    
    def _determine_winner(self) -> None:
        """Assigns to `self.winner` the correct winner at this state.
        """
        if self._is_winner(self.X_table):
            self.winner = State.X
        elif self._is_winner(self.O_table):
            self.winner = State.O
        elif self._is_terminal():
            self.winner = State.DRAW
        else:
            self.winner = State.UNDETERMINED
    
    def _is_winner(self, arr: Tuple[Tuple[bool, ...], ...]) -> bool:
        """Checks in the following directions at each cell:
        1. Rightwards
        2. Right-downwards
        3. Downwards
        4. Left-downwards
        """
        for row in range(height):
            for col in range(width):
                if self._is_direction_winning(arr, row, col, (0, 1)):
                    return True
                elif self._is_direction_winning(arr, row, col, (1, 1)):
                    return True
                elif self._is_direction_winning(arr, row, col, (1, 0)):
                    return True
                elif self._is_direction_winning(arr, row, col, (1, -1)):
                    return True
        return False
    
    def _is_direction_winning(self, arr: Tuple[Tuple[bool, ...], ...], row: int, col: int,
                              dir: Tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]) -> bool:
        end_row = row + dir[0] * (connect - 1)
        end_col = col + dir[1] * (connect - 1)
        if end_row < 0 or end_row >= height or end_col < 0 or end_col >= width:
            return False
        
        for i in range(connect):
            if not arr[row + dir[0] * i][col + dir[1] * i]:
                return False
        return True
    
    def _is_terminal(self) -> bool:
        for row in range(height):
            for col in range(width):
                if not self.X_table[row][col] and not self.O_table[row][col]:
                    return False
        return True
    
    def move(self, col: int) -> "Board":
        """Makes a move at the indicated column.
        Returns a new instance of `Board`.
        """
        for row in range(height):
            if self.X_table[row][col] or self.O_table[row][col]:
                continue
            if self.is_X_turn:
                new_X_table = tuple(
                    tuple(
                        True if i == row and j == col else cell for j, cell in enumerate(table_row)
                    ) for i, table_row in enumerate(self.X_table)
                )
                new_O_table = self.O_table
            else:
                new_X_table = self.X_table
                new_O_table = tuple(
                    tuple(
                        True if i == row and j == col else cell for j, cell in enumerate(table_row)
                    ) for i, table_row in enumerate(self.O_table)
                )
            return Board(is_X_turn=not self.is_X_turn, X_table=new_X_table, O_table=new_O_table)
        
        assert False, "Invalid move!"
    
    def __repr__(self):
        board_string = ""
        for row in range(height - 1, -1, -1):
            row_string = ""
            for col in range(width):
                assert not self.X_table[row][col] or not self.O_table[row][col]
                if self.X_table[row][col]:
                    row_string += "X "
                elif self.O_table[row][col]:
                    row_string += "O "
                else:
                    row_string += "_ "
            board_string += row_string + "\n"
        return board_string

    def __str__(self):
        return self.__repr__()
