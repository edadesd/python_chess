from enum import Enum


MIN_RANK = 1
MAX_RANK = 8
MIN_FILE = "a"
MAX_FILE = "h"
RANKS = (1, 2, 3, 4, 5, 6, 7, 8)
FILES = ("a", "b", "c", "d", "e", "f", "g", "h")
FIRST_RANK_LIGHT = ("b", "d", "f", "h")


class Color(Enum):
    LIGHT = 1
    DARK = 2

class Space:

    def __init__(self, file, rank):

        if(rank in RANKS) and (file in FILES):
            self.rank = rank
            self.file = file
            self.name = file + str(rank)
        else:
            raise ValueError()

        if self.rank % 2 == 0:

            # Even ranks for which the first rank in the file is light are themselves dark.
            # e.g. h1 is light; h2, h4, h6, and h8 are dark.
            if self.file in FIRST_RANK_LIGHT:
                self.color = Color.DARK

            # Even ranks for which the first rank in the file is dark are themselves light.
            # e.g. a1 is dark; a2, a4, a6, and a8 are light.
            else:
                self.color = Color.LIGHT

        else:

            # Odd ranks for which the first rank in the file is light are themselves light.
            # e.g. h1 is light; h3, h5, and h7 are also light.
            if self.file in FIRST_RANK_LIGHT:
                self.color = Color.LIGHT

            # Odd ranks for which the first rank in the file is dark are themselves dark.
            # e.g. a1 is dark; a3, a5, and a7 are also dark.
            else:
                self.color = Color.DARK

        self.current_piece = None


class Board:
    """"
    The Board is represented as a list of lists. Each sub-list represents a file, and each file has a Space
    for each rank on the board. This makes the Board an 8x8 grid, each file name in algebraic notation corresponding
    to a row in the grid.
    """

    def __init__(self):
        self.spaces = []

        for file in FILES:
            new_file = []
            for rank in RANKS:
                new_file.append(Space(file, rank))
            self.spaces.append(new_file)



    def get_space(self, file, rank):
        """
        Gets a Space by converting the arguments into the coordinates of the Space in the board's grid.
        Although files represent columns on the board and Cartesian coordinates are specified in (x, y)
        format, having the first argument be file here lets the argument take the form of algebraic notation
        which lists the file first (e.g. a1 instead of 1a.)
        """

        # Map file names to list element numbers

        files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        rank_position = rank - 1

        try:
            target_space = self.spaces[files[file]][rank_position]
        except IndexError:
            target_space = None

        return target_space