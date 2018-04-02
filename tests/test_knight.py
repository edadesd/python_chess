"""
Tests for the Knight class to ensure correct
placement, movement, capturing, and promotion
behavior, as well as correct attributes upon creation.

Last modified: 4/2/2018
Author: Daniel Edades
"""

import sys
import pytest
import random
sys.path.append("..")
from board import Board
from knight import Knight
from piece import PieceColor
from piece import IllegalPlacementException
from piece import IllegalMoveException


@pytest.fixture
def test_board():
    test_board = Board()
    return test_board


@pytest.fixture
def test_white_knight(test_board):
    starting_file = "b"
    starting_rank = 1
    starting_space = test_board.get_space(starting_file, starting_rank)
    test_knight = Knight(PieceColor.WHITE)
    return test_knight


class TestCreateKnight:
    def test_create_knight(self, test_board, test_white_knight):
        assert test_white_knight