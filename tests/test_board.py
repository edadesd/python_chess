"""
Tests for the Board class to ensure that
a Board is created properly when constructed
with Board().

Last Modified: 3/29/2018
Author: Daniel Edades
"""

import sys
import pytest
sys.path.append("..")
from board import Board
from board import Color

ranks = (1, 2, 3, 4, 5, 6, 7, 8)
files = ("a", "b", "c", "d", "e", "f", "g", "h")
FIRST_RANK_LIGHT = ("b", "d", "f", "h")


class TestBoard:

    def test_spaces(self):

        test_board = Board()

        # Check that the passed board exists
        assert test_board
        assert test_board.spaces

        # Check that the passed Board has the correct number of files
        assert len(test_board.spaces) == len(files)

        # Check that the passed Board has the correct number of Spaces
        expected_num_spaces = len(ranks) * len(files)
        total_len = 0
        for file in test_board.spaces:

            # Check that the file has the correct number of ranks
            assert len(file) == len(ranks)
            total_len += len(file)

        assert total_len == expected_num_spaces

        # Check that all of the expected Spaces are in the Board
        for file in files:
            for rank in ranks:
                expected_name = file + str(rank)
                retrieved_space = test_board.get_space(file, rank)

                # Get the Space and check that it exists
                assert retrieved_space

                # Check that the retrieved Space has the appropriate rank, file, and name
                assert retrieved_space.rank == rank
                assert retrieved_space.file == file
                assert retrieved_space.name == expected_name

                # Check that the retrieved Space has no current Piece on it

                assert not retrieved_space.current_piece

                # Check that the retrieved Space has a Color
                assert retrieved_space.color

                # Check that the retrieved space has the correct Color
                if file in FIRST_RANK_LIGHT:
                    if rank % 2 != 0:
                        expected_color = Color.LIGHT
                    else:
                        expected_color = Color.DARK
                else:
                    if rank % 2 == 0:
                        expected_color = Color.LIGHT
                    else:
                        expected_color = Color.DARK

                assert retrieved_space.color == expected_color

