from enum import Enum
from board import Space

class PieceColor(Enum):
    WHITE = 1
    BLACK = -1


class IllegalMoveException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


class IllegalPlacementException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


class Piece:

    def __init__(self, color):
        self.color = color
        self.moved = False
        self.current_space = None

    def move(self, target):

        if not isinstance(target, Space):
            raise IllegalPlacementException("The target is not a Space.")

        if self.current_space and not target.current_piece:
            self.current_space = target
            target.current_piece = self
            self.moved = True
        else:
            raise IllegalMoveException("Target space not empty.")

    def capture(self, target):
        if self.current_space and target.current_piece and (self.color != target.current_piece.color):
            target.current_piece.remove()
            target.current_piece = self
            self.current_space = target
            self.moved = True
        else:
            if not self.current_space:
                raise IllegalMoveException("That piece is not on the board.")
            elif not target.current_piece:
                raise IllegalMoveException("There is no piece to capture in the target space.")
            elif self.color == target.current_piece.color:
                raise IllegalMoveException("Cannot capture pieces of a player's own color.")

    def place(self, target):

        if target:
            if not target.current_piece:
                if self.current_space:
                    self.current_space.current_piece = None
                target.current_piece = self
                self.current_space = target
            elif target.current_piece:
                raise IllegalPlacementException("There is already a piece on that space.")

        elif not target:
            raise IllegalPlacementException("The target is not a Space.")

    def remove(self):
        if self.current_space:
            self.current_space.current_piece = None
            self.current_space = None
        else:
            raise IllegalMoveException("That piece is not on the board.")
