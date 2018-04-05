"""
Tests for the Rook class to ensure correct
placement, movement, and capturing,
as well as correct attributes upon creation.

Last modified: 4/5/2018
Author: Daniel Edades
"""

import sys
import pytest
import random
sys.path.append("..")
from board import *
from rook import Rook
from piece import PieceColor
from piece import IllegalPlacementException
from piece import IllegalMoveException


@pytest.fixture
def test_board():
    test_board = Board()
    return test_board

@pytest.fixture
def test_white_rook(test_board):
    assert test_board
    test_white_rook = Rook(PieceColor.WHITE)
    starting_space = test_board.get_space("a", 1)
    test_white_rook.place(starting_space)

    return test_white_rook

@pytest.fixture
def test_white_rook(test_board):
    starting_file = "a"
    starting_rank = 1
    starting_space = test_board.get_space(starting_file, starting_rank)
    test_rook = Rook(PieceColor.WHITE)
    test_rook.place(starting_space)
    return test_rook

@pytest.fixture
def test_black_rook(test_board):
    starting_file ="a"
    starting_rank = 8
    starting_space = test_board.get_space(starting_file, starting_rank)
    test_rook = Rook(PieceColor.BLACK)
    test_rook.place(starting_space)
    return test_rook


class TestCreateRook:

    def test_create_white_rook(self, test_board):
        test_rook = Rook(PieceColor.WHITE)
        starting_file = "a"
        starting_rank = 1
        starting_space = test_board.get_space(starting_file, starting_rank)
        test_rook.place(starting_space)

        assert test_rook.current_space is starting_space

    def test_create_black_rook(self, test_board):
        test_rook = Rook(PieceColor.BLACK)
        starting_file = "a"
        starting_rank = 8
        starting_space = test_board.get_space(starting_file, starting_rank)


class TestMoveRook:

    def test_move_rook_horizontal(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        assert ord(test_white_rook.current_space.file) < ord(MAX_FILE)

        target_space = test_board.get_space(MAX_FILE, test_white_rook.current_space.rank)
        test_white_rook.move(test_board, target_space)
        assert test_white_rook.current_space is target_space

    def test_move_rook_vertical(self, test_board, test_black_rook):
        assert test_board
        assert test_black_rook
        assert test_black_rook.current_space
        assert test_black_rook.current_space.rank > MIN_RANK

        target_space = test_board.get_space(test_black_rook.current_space.file, MIN_RANK)
        test_black_rook.move(test_board, target_space)
        assert test_black_rook.current_space is target_space

    def bad_rook_move_horizontal(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        assert ord(test_white_rook.current_space.file) + 1 < ord(MAX_FILE)

        target_space = test_board.get_space(MAX_FILE, test_white_rook.current_space.rank)
        obstacle_space = test_board.get_space(chr(ord(MAX_FILE) - 1), test_white_rook.current_space.rank)
        obstacle_piece = Rook(PieceColor.BLACK)
        obstacle_piece.place(obstacle_space)

        test_white_rook.move(test_board, target_space)

    def test_bad_rook_move_horizontal(self, test_board, test_white_rook):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_rook_move_horizontal(test_board, test_white_rook)