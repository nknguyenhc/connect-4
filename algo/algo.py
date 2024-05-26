from time import time

from board import Board
from .node import MctsNode

class Algo:
    def __init__(self):
        self.root: MctsNode = None
    
    def next_move(self, board: Board, time_control: float) -> int:
        self.root = MctsNode(board)
        start_time = time()
        end_time = start_time + time_control
        while time() < end_time:
            self._search()
        return self.root.best_move()
    
    def _search(self) -> None:
        leaf = self.root.select()
        child = leaf.expand()
        value = child.simulate()
        child.back_propagates(value)
