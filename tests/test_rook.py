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

    def test_move_rook_horizontal_right(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        assert ord(test_white_rook.current_space.file) < ord(MAX_FILE)

        target_space = test_board.get_space(MAX_FILE, test_white_rook.current_space.rank)
        test_white_rook.move(test_board, target_space)
        assert test_white_rook.current_space is target_space

    def test_move_rook_horizontal_left(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        starting_space = test_board.get_space(MAX_FILE, MIN_RANK)
        test_white_rook.place(starting_space)

        target_space = test_board.get_space(MIN_FILE, MIN_RANK)
        test_white_rook.move(test_board, target_space)
        assert test_white_rook.current_space is target_space

    def test_move_rook_vertical_down(self, test_board, test_black_rook):
        assert test_board
        assert test_black_rook
        assert test_black_rook.current_space
        assert test_black_rook.current_space.rank > MIN_RANK

        target_space = test_board.get_space(test_black_rook.current_space.file, MIN_RANK)
        test_black_rook.move(test_board, target_space)
        assert test_black_rook.current_space is target_space

    def test_move_rook_vertical_up(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        assert test_white_rook.current_space.rank < MAX_RANK

        target_space = test_board.get_space(test_white_rook.current_space.file, MAX_RANK)
        test_white_rook.move(test_board, target_space)
        assert test_white_rook.current_space is target_space


    # A Rook should not be able to move over any other pieces

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
        assert("A Rook cannot move over any other piece.") in str(info)

    def bad_rook_move_vertical(self, test_board, test_black_rook):
        assert test_board
        assert test_black_rook
        assert test_black_rook.current_space
        assert test_black_rook.current_space.rank - 1 > MIN_RANK

        target_space = test_board.get_space(test_black_rook.current_space.file, MIN_RANK)
        obstacle_space = test_board.get_space(test_black_rook.current_space.file, MIN_RANK + 1)
        obstacle_piece = Rook(PieceColor.WHITE)
        obstacle_piece.place(obstacle_space)

        test_black_rook.move(test_board, target_space)

    def test_bad_rook_move_vertical(self, test_board, test_black_rook):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_rook_move_vertical(test_board, test_black_rook)
        assert "A Rook cannot move over any other piece." in str(info)

    # A Rook should not be able to move diagonally

    def bad_rook_move_diagonal(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        assert test_white_rook.current_space.rank + 1 <= MAX_RANK
        assert ord(test_white_rook.current_space.file) <= ord(MAX_FILE)

        target_rank = test_white_rook.current_space.rank + 1
        target_file = chr(ord(test_white_rook.current_space.file) + 1)
        target_space = test_board.get_space(target_file, target_rank)

        test_white_rook.move(test_board, target_space)

    def test_bad_rook_move_diagonal(self, test_board, test_white_rook):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_rook_move_diagonal(test_board, test_white_rook)
        assert "A rook must move entirely vertically or entirely horizontally." in str(info)

    # A Rook should not be able to move in an L pattern of any dimensions

    def bad_rook_move_large_l(self, test_board, test_white_rook):
        assert test_board
        assert test_white_rook
        assert test_white_rook.current_space
        current_space = test_white_rook.current_space
        # Place the test Rook on a1
        if current_space.rank != MIN_RANK or current_space.file != MIN_FILE:
            test_white_rook.place(MIN_FILE, MIN_RANK)

        assert test_white_rook.current_space is test_board.get_space(MIN_FILE, MIN_RANK)

        # Move the test Rook to g8, which makes a large L but not a diagonal move.
        test_white_rook.move(test_board, test_board.get_space(chr(ord(MAX_FILE) - 1), MAX_RANK))

    def test_bad_rook_move_large_l(self, test_board, test_white_rook):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_rook_move_large_l(test_board, test_white_rook)
        assert "A rook must move entirely vertically or entirely horizontally." in str(info)