import unittest

from .board import Board, State
from config import width

class BoardTest(unittest.TestCase):
    def test_empty(self):
        board = Board()
        self.assertEqual([i for i in range(width)], board.actions())
        self.assertEqual(State.UNDETERMINED, board.winner)
    
    def test_undetermined(self):
        board = Board()
        board = board.move(0)
        board = board.move(1)
        board = board.move(0)
        self.assertEqual([i for i in range(width)], board.actions())
        self.assertEqual(State.UNDETERMINED, board.winner)
    
    def test_horizontal_win(self):
        board = Board()
        board = board.move(0)
        board = board.move(0)
        board = board.move(1)
        board = board.move(1)
        board = board.move(2)
        board = board.move(2)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(3)
        self.assertEqual(State.X, board.winner)

        board = Board()
        board = board.move(0)
        board = board.move(1)
        board = board.move(1)
        board = board.move(2)
        board = board.move(2)
        board = board.move(3)
        board = board.move(3)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(4)
        self.assertEqual(State.O, board.winner)
    
    def test_vertical_win(self):
        board = Board()
        board = board.move(0)
        board = board.move(1)
        board = board.move(0)
        board = board.move(2)
        board = board.move(0)
        board = board.move(3)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(0)
        self.assertEqual(State.X, board.winner)

        board = Board()
        board = board.move(0)
        board = board.move(5)
        board = board.move(0)
        board = board.move(5)
        board = board.move(1)
        board = board.move(5)
        board = board.move(1)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(5)
        self.assertEqual(State.O, board.winner)
    
    def test_diagonal_win(self):
        board = Board()
        board = board.move(3)
        board = board.move(4)
        board = board.move(5)
        board = board.move(5)
        board = board.move(4)
        board = board.move(6)
        board = board.move(5)
        board = board.move(6)
        board = board.move(0)
        board = board.move(6)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(6)
        self.assertEqual(State.X, board.winner)
    
    def test_draw(self):
        board = Board()
        for i in range(6):
            for j in range(3):
                if i % 2 == 0:
                    board = board.move(j)
                    board = board.move(3 + j)
                else:
                    board = board.move(3 + j)
                    board = board.move(j)
        for i in range(6):
            board = board.move(6)
        self.assertEqual(State.DRAW, board.winner)
    
    def test_filled(self):
        board = Board()
        for i in range(6):
            board = board.move(2)
        self.assertEqual({0, 1, 3, 4, 5, 6}, set(board.actions()))
    
    def test_steal(self):
        board = Board()
        board = board.move(4)
        board = board.move(-1)
        board = board.move(3)
        board = board.move(4)
        board = board.move(2)
        board = board.move(4)
        board = board.move(1)
        self.assertEqual(State.UNDETERMINED, board.winner)
        board = board.move(4)
        self.assertEqual(State.O, board.winner)
    
    def test_compact_string(self):
        board = Board()
        board = board.move(0)
        board = board.move(0)
        board = board.move(1)
        board = board.move(3)
        board = board.move(1)
        expected = "X X _ O _ _ _  O X _ _ _ _ _  _ _ _ _ _ _ _  _ _ _ _ _ _ _  _ _ _ _ _ _ _  _ _ _ _ _ _ _|F"
        self.assertEqual(board.to_compact_string(), expected)
        self.assertEqual(board, Board.from_string(expected))
