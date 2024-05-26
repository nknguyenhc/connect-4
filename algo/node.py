from random import randint
import math
from typing import List

from board import Board, State

class MctsNode:
    WIN = 1
    C = 1.4

    def __init__(self, board: Board, parent: "MctsNode"=None, move: int=None):
        self.N: int = 0
        self.U: float = 0
        self.board: Board = board
        self.parent: "MctsNode" = parent
        self.move: int = move
        self.children: List["MctsNode"] = None
    
    def _ucb(self) -> float:
        if self.N == 0:
            return float('inf')
        return -self.U / self.N + math.sqrt(math.log(self.parent.N) / self.N)
    
    def select(self) -> "MctsNode":
        if self.children is None:
            return self
        
        best_child: "MctsNode" = None
        for child in self.children:
            if best_child is None or best_child._ucb() < child._ucb():
                best_child = child
        assert best_child is not None
        return best_child.select()
    
    def expand(self) -> "MctsNode":
        assert self.children is None
        if self.board.winner != State.UNDETERMINED:
            return self
        
        actions = self.board.actions()
        self.children = []
        for action in actions:
            self.children.append(MctsNode(self.board.move(action), parent=self, move=action))
        
        index = randint(0, len(actions))
        return self.children[index]
    
    def simulate(self) -> float:
        board = self.board
        while board.winner == State.UNDETERMINED:
            actions = board.actions()
            index = randint(0, len(actions))
            board = board.move(actions[index])
        
        if board.winner == State.DRAW:
            return 0
        side = State.X if self.board.is_X_turn else State.O
        return MctsNode.WIN if board.winner == side else -MctsNode.WIN
    
    def back_propagates(self, utility) -> None:
        self.N += 1
        self.U += utility
        if self.parent is not None:
            self.parent.back_propagates(-utility)
    
    def _best_child(self) -> "MctsNode":
        if self.children is None:
            return None
        
        best_child: "MctsNode" = None
        for child in self.children:
            if best_child is None or best_child.N < child.N:
                best_child = child
        assert best_child is not None
        return best_child
    
    def best_move(self):
        return self._best_child().move
