from typing import Literal, List, Tuple
from copy import deepcopy
import numpy as np

from config import height, width, connect, steal

class State:
    UNDETERMINED = 0
    X = 1
    O = 2
    DRAW = 3

class InvalidBoardStringException(Exception):
    """Representing an exception raised when an invalid string is provided
    in the factory method of `Board` class.
    """
    def __init__(self, message: str):
        """Instantiates a new exception,
        raised when an invalid string is provided to create a new `Board`.
        """
        super().__init__(message)

class Board:
    def __init__(self, is_X_turn: bool=True,
                 X_table: np.ndarray=None, O_table: np.ndarray=None,
                 move_count: int=0,
                 ):
        """Instantiates a new table.
        Either:
        1. Both `X_table` and `O_table` are left blank, or
        2. Both `X_table` and `O_table` are provided with the correct dimension.
        """
        if X_table is not None and O_table is not None:
            self.X_table = X_table
            self.O_table = O_table
        else:
            self.X_table = np.array(tuple(tuple(False for _ in range(width)) for _ in range(height)))
            self.O_table = np.array(tuple(tuple(False for _ in range(width)) for _ in range(height)))
        self.is_X_turn = is_X_turn
        self.move_count = move_count
        self._determine_winner()
    
    def actions(self) -> List[int]:
        """Returns the set of possible actions in this state.
        Each action is an int indicating the column to move at.
        """
        actions: List[int] = []
        for col in range(width):
            if self._is_column_movable(col):
                actions.append(col)
        if self.move_count == 1 and steal:
            actions.append(-1)
        return actions
    
    def is_valid_action(self, col: int) -> bool:
        """Determines if the action is valid.
        Only to be used when interacting with the user.
        """
        if col == -1:
            return self.move_count == 1 and steal and not self.is_X_turn
        return col >= 0 and col < width and self._is_column_movable(col)

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
    
    def _is_direction_winning(self, arr: np.ndarray, row: int, col: int,
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
        if col == -1:
            assert self.move_count == 1 and steal and not self.is_X_turn
            new_O_table = deepcopy(self.X_table)
            new_X_table = np.array(
                tuple(tuple(False for _ in range(width)) for _ in range(height)))
            return Board(is_X_turn=True, X_table=new_X_table, O_table=new_O_table, move_count=2)
        for row in range(height):
            if self.X_table[row][col] or self.O_table[row][col]:
                continue
            if self.is_X_turn:
                new_X_table = np.array(tuple(
                    tuple(
                        True if i == row and j == col else cell for j, cell in enumerate(table_row)
                    ) for i, table_row in enumerate(self.X_table)
                ))
                new_O_table = self.O_table
            else:
                new_X_table = self.X_table
                new_O_table = np.array(tuple(
                    tuple(
                        True if i == row and j == col else cell for j, cell in enumerate(table_row)
                    ) for i, table_row in enumerate(self.O_table)
                ))
            return Board(is_X_turn=not self.is_X_turn, X_table=new_X_table, O_table=new_O_table, move_count=self.move_count + 1)
        
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
    
    def from_string(string: str) -> "Board":
        """Returns a board represented by the string.
        The string is the same as the string representation of the board,
        but combined into one line, lines are separated by two space characters.
        """
        parts = string.split('|')
        if len(parts) != 2:
            raise InvalidBoardStringException("Incorrect number of parts by |, expect 2")

        match parts[1]:
            case "T":
                is_X_turn = True
            case "F":
                is_X_turn = False
            case _:
                raise InvalidBoardStringException(f"Incorrect turn token \"{parts[1]}\"")
        
        string = parts[0]

        items = string.split('  ')
        if len(items) != height:
            raise InvalidBoardStringException("Incorrect number of lines")
        
        X_table: List[Tuple[bool, ...]] = []
        O_table: List[Tuple[bool, ...]] = []
        move_count: int = 0
        for row in items:
            X_row: List[bool] = []
            O_row: List[bool] = []
            cells = row.split(' ')
            if len(cells) != width:
                raise InvalidBoardStringException(f"Incorrect number of items in a line: {row}")
            
            for cell in cells:
                match cell:
                    case "X":
                        X_row.append(True)
                        O_row.append(False)
                        move_count += 1
                    case "O":
                        X_row.append(False)
                        O_row.append(True)
                        move_count += 1
                    case "_":
                        X_row.append(False)
                        O_row.append(False)
                    case _:
                        raise InvalidBoardStringException(f"Invalid character \"{cell}\"")
            
            X_table.append(tuple(X_row))
            O_table.append(tuple(O_row))
        
        return Board(is_X_turn=is_X_turn,
                     X_table=np.array(tuple(X_table)),
                     O_table=np.array(tuple(O_table)),
                     move_count=move_count)
    
    def to_compact_string(self) -> str:
        board_string = ""
        for row in range(height):
            row_string = ""
            for col in range(width):
                if self.X_table[row][col]:
                    row_string += "X"
                elif self.O_table[row][col]:
                    row_string += "O"
                else:
                    row_string += "_"
                if col != width - 1:
                    row_string += " "
            board_string += row_string
            if row != height - 1:
                board_string += "  "
        if self.is_X_turn:
            board_string += "|T"
        else:
            board_string += "|F"
        return board_string
    
    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.is_X_turn == other.is_X_turn and \
            (self.X_table == other.X_table).all() and \
            (self.O_table == other.O_table).all()
