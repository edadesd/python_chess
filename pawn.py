"""
Pawn class
Pawns start on the second rank of each file for the
White player and the seventh rank of each file for the
Black player. With their first move, they can move one
or two spaces forward (with the White player traveling
up the board and the Black player traveling down the
board.) For subsequent moves, a pawn may only move one space.

A pawn must capture diagonally ahead, meaning that it
cannot move straight forward onto an occupied space. It can
also never jump over any other piece, nor move backward.

When a pawn reaches the last rank (8 for the White player,
1 for the Black player) it must promote into another piece.

Last modified: 3/29/2018
Author: Daniel Edades
"""

from piece import *
from board import *
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = -1

class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color)

    def move(self, board, target):
        """
        If a pawn has not already moved, it may move one or two spaces up.
        If a pawn has already moved, it may only move one space vertically.
        """

        if self.current_space:
            current_rank = self.current_space.rank
            current_file = self.current_space.file
            direction = 0

            # The direction a Pawn moves depends on its color. White Pawns move up (i.e. from lower ranks to
            # higher ranks) while black Pawns move down, from higher ranks to lower ranks. Thus, the difference
            # between a black Pawn's ending and starting ranks will be negative. Multiply this by -1 to
            # turn it into a positive value. If the result is negative, the Pawn attempted to move backward.

            if self.color == PieceColor.WHITE:
                direction = Direction.UP.value
            else:
                direction = Direction.DOWN.value

            # Pawn moves two Spaces on first move
            if not self.moved and direction * (target.rank - current_rank) == 2 and target.file == current_file:

                next_space = board.get_space(self.current_space.file, self.current_space.rank + direction)
                second_space = board.get_space(next_space.file, next_space.rank + (2 * direction))

                if next_space.current_piece is None and second_space.current_piece is None:
                    super().move(target)

                else:
                    if second_space.current_piece:
                        raise IllegalMoveException("A Pawn may only capture diagonally.")
                    elif next_space.current_piece:
                        raise IllegalMoveException("A Pawn may not jump over any other pieces.")

            # Pawn tries to move two Spaces after first move
            elif self.moved and direction * (target.rank - current_rank) == 2 and target.file == current_file:

                raise IllegalMoveException("A Pawn may only move two Spaces on its first move.")

            # Pawn moves one space
            elif direction * (target.rank - current_rank) == 1 and current_file == target.file:

                next_space = board.get_space(self.current_space.file, direction * self.current_space.rank + direction)
                super().move(target)

            # Pawn tried to move laterally or diagonally
            elif target.file != current_file:
                raise IllegalMoveException("A Pawn may not move to a different file unless capturing.")

            # Pawn tried to move mo
            elif direction * (target.rank - current_rank) > 2:
                raise IllegalMoveException("A Pawn may never move more than two Spaces at a time.")

            elif direction * (target.rank - current_rank) == 0:
                raise IllegalMoveException("A Pawn must end up on a different Space from the one it started on when" +
                                           " moving.")

            elif direction * (target.rank - current_rank) < 0:
                raise IllegalMoveException("A Pawn may not move backward.")

        else:
            raise super().IllegalMoveException("That piece is not on the board.")

    def capture(self, board, target):
        pass

    def promote(self, board, target):
        pass

