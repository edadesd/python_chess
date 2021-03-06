from piece import *
from board import *


class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)

    def move(self, board, target):

        if target.file == self.current_space.file or target.rank == self.current_space.rank:
            if target.file == self.current_space.file and target.rank == self.current_space.rank:
                raise IllegalMoveException("A piece that moves must end on a different space.")
            else:
                # Determine whether move is horizontal or vertical.
                if target.file != self.current_space.file:

                    # Horizontal move
                    distance = ord(target.file) - ord(self.current_space.file)

                    traveled = 0
                    legal_move = True

                    while traveled < abs(distance) and legal_move:
                        # Moving in toward the H-file
                        if distance > 0:
                            target_file = chr(ord(self.current_space.file) + traveled + 1)
                        # Moving toward the A-file
                        elif distance < 0:
                            target_file = chr(ord(self.current_space.file) - traveled - 1)
                        target_space = board.get_space(target_file, self.current_space.rank)
                        if target_space.current_piece:
                            legal_move = False
                        else:
                            traveled += 1
                    if legal_move:
                        super().move(target)
                    else:
                        raise IllegalMoveException("A Rook cannot move over any other piece.")

                elif target.rank != self.current_space.rank:

                    # Vertical move
                    distance = target.rank - self.current_space.rank
                    traveled = 0

                    legal_move = True

                    while traveled < abs(distance) and legal_move:
                        if distance > 0:
                            # Moving toward rank 8
                            target_rank = self.current_space.rank + traveled + 1

                            # Moving toward rank 1
                        elif distance < 0:
                            target_rank = self.current_space.rank - traveled - 1
                        target_space = board.get_space(self.current_space.file, target_rank)
                        if target_space.current_piece:
                            legal_move = False
                        else:
                            traveled += 1
                    if legal_move:
                        super().move(target)
                    else:
                        raise IllegalMoveException("A Rook cannot move over any other piece.")
                else:
                    raise IllegalMoveException("A rook must move entirely vertically or entirely horizontally.")
        else:
            raise IllegalMoveException("A rook must move entirely vertically or entirely horizontally.")
