from piece import *
from board import *
from enum import Enum


class Knight(Piece):

    def __init__(self, color):
        super().__init__(color)

    def move(self, target):
        """
        A knight must move in one of the following ways:
        Up or down two ranks, and left or right one file
        Left or right two files, and up or down one rank
        """
        current = self.current_space
        vertical_moved = abs(target.rank - current.rank)
        horizontal_moved = abs(ord(target.file) - ord(current.file))
        if (vertical_moved == 2 and horizontal_moved == 1 or
                vertical_moved == 1 and horizontal_moved == 2):
                super().move(target)
        else:
            raise IllegalMoveException("A Knight must move two spaces straight and one space perpendicular.")
