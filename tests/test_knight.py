"""
Tests for the Knight class to ensure correct
placement, movement, and capturing,
as well as correct attributes upon creation.

Last modified: 4/3/2018
Author: Daniel Edades
"""

import sys
import pytest
import random
sys.path.append("..")
from board import *
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
    test_knight.place(starting_space)
    return test_knight


@pytest.fixture
def test_black_knight(test_board):
    starting_file = "b"
    starting_rank = 8
    starting_space = test_board.get_space(starting_file, starting_rank)
    test_knight = Knight(PieceColor.BLACK)
    test_knight.place(starting_space)
    return test_knight


class TestCreateKnight:

    def test_create_white_knight(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.color is PieceColor.WHITE
        starting_file = "g"
        starting_rank = 1
        starting_space = test_board.get_space(starting_file, starting_rank)
        test_white_knight.place(starting_space)
        assert test_white_knight.current_space is starting_space


    def test_create_black_knight(self, test_board, test_black_knight):
        assert test_black_knight
        assert test_black_knight.color is PieceColor.BLACK
        starting_file = "g"
        starting_rank = 8
        starting_space = test_board.get_space(starting_file, starting_rank)
        test_black_knight.place(starting_space)
        assert test_black_knight.current_space is starting_space


class TestMoveKnight:

    # Test that the Knight can move two ranks up and one file to the left on a board with no other pieces.
    def test_move_knight_up_left(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.current_space
        assert test_white_knight.current_space.rank + 2 <= MAX_RANK
        assert ord(test_white_knight.current_space.file) > ord(MIN_FILE)

        current_space = test_white_knight.current_space
        target_file = chr(ord(current_space.file) - 1)
        target_rank = current_space.rank + 2
        target_space = test_board.get_space(target_file, target_rank)

        test_white_knight.move(target_space)
        assert test_white_knight.current_space is target_space

    # Test that the Knight can move two ranks up and one file to the right on a board with no other pieces.
    def test_move_knight_up_right(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.current_space
        assert test_white_knight.current_space.rank + 2 <= MAX_RANK
        assert ord(test_white_knight.current_space.file) < ord(MAX_FILE)

        current_space = test_white_knight.current_space
        target_file = chr(ord(current_space.file) + 1)
        target_rank = current_space.rank + 2
        target_space = test_board.get_space(target_file, target_rank)

        test_white_knight.move(target_space)
        assert test_white_knight.current_space is target_space

    # Test that the Knight can move two ranks down and one file to the left on a board with no other pieces.
    def test_move_knight_down_left(self, test_board, test_black_knight):
        assert test_board
        assert test_black_knight
        assert test_black_knight.current_space
        assert test_black_knight.current_space.rank - 2 >= MIN_RANK
        assert ord(test_black_knight.current_space.file) > ord(MIN_FILE)

        current_space = test_black_knight.current_space
        target_file = chr(ord(current_space.file) - 1)
        target_rank = current_space.rank - 2
        target_space = test_board.get_space(target_file, target_rank)

        test_black_knight.move(target_space)
        assert test_black_knight.current_space is target_space

    # Test that the Knight can move two ranks down and one file to the right on a board with no other pieces.
    def test_move_knight_down_right(self, test_board, test_black_knight):
        assert test_board
        assert test_black_knight
        assert test_black_knight.current_space
        assert test_black_knight.current_space.rank - 2 >= MIN_RANK
        assert ord(test_black_knight.current_space.file) < ord(MAX_FILE)

        current_space = test_black_knight.current_space
        target_file = chr(ord(current_space.file) + 1)
        target_rank = current_space.rank - 2
        target_space = test_board.get_space(target_file, target_rank)

        test_black_knight.move(target_space)
        assert test_black_knight.current_space is target_space

    # Test that the Knight can move two files right and one file up on a board with no other pieces.
    def test_move_knight_right_up(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.current_space
        assert test_white_knight.current_space.rank + 1 <= MAX_RANK
        assert ord(test_white_knight.current_space.file) + 2 <= ord(MAX_FILE)

        current_space = test_white_knight.current_space
        target_file = chr(ord(current_space.file) + 2)
        target_rank = current_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)

        test_white_knight.move(target_space)
        assert test_white_knight.current_space is target_space

    # Test that the Knight can move two files right and one file down on a board with no other pieces.
    def test_move_knight_right_down(self, test_board, test_black_knight):
        assert test_board
        assert test_black_knight
        assert test_black_knight.current_space
        assert test_black_knight.current_space.rank - 1 >= MIN_RANK
        assert ord(test_black_knight.current_space.file) + 2 <= ord(MAX_FILE)

        current_space = test_black_knight.current_space
        target_file = chr(ord(current_space.file) + 2)
        target_rank = current_space.rank - 1
        target_space = test_board.get_space(target_file, target_rank)

        test_black_knight.move(target_space)
        assert test_black_knight.current_space is target_space

    # Test that the Knight can move two files left and one file up on a board with no other pieces.
    def test_move_knight_left_up(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        new_starting_space = test_board.get_space("g", 1)
        test_white_knight.place(new_starting_space)
        assert test_white_knight.current_space is new_starting_space
        assert ord(test_white_knight.current_space.file) - 2 >= ord(MIN_FILE)
        assert test_white_knight.current_space.rank + 1 <= MAX_RANK

        target_file = chr(ord(new_starting_space.file) - 2)
        target_rank = new_starting_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)

        test_white_knight.move(target_space)
        assert test_white_knight.current_space is target_space

    # Test that the Knight can move two files left and one file down on a board with no other pieces.
    def test_move_knight_left_down(self, test_board, test_black_knight):
        assert test_board
        assert test_black_knight
        new_starting_space = test_board.get_space("g", 8)
        test_black_knight.place(new_starting_space)
        assert test_black_knight.current_space is new_starting_space
        assert ord(test_black_knight.current_space.file) - 2 >= ord(MIN_FILE)
        assert test_black_knight.current_space.rank - 1 >= MIN_RANK

        target_file = chr(ord(new_starting_space.file) - 2)
        target_rank = new_starting_space.rank - 1
        target_space = test_board.get_space(target_file, target_rank)

        test_black_knight.move(target_space)
        assert test_black_knight.current_space is target_space

    def bad_knight_move(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.current_space

        # Choose a target Space that is not a legal Knight move away from the test Knight's current Space.
        current_space = test_white_knight.current_space
        target_rank = test_white_knight.current_space.rank + 1
        target_space = test_board.get_space(test_white_knight.current_space.file, target_rank)

        # Attempt to move the Knight to the target space, expecting this to cause an IllegalMoveException
        test_white_knight.move(target_space)

    def test_bad_knight_move(self, test_board, test_white_knight):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_knight_move(test_board, test_white_knight)
            assert "A Knight must move two spaces straight and one space perpendicular." in str(info)

    def test_knight_jump(self, test_board, test_white_knight):
        assert test_board
        assert test_white_knight
        assert test_white_knight.current_space

        # Place Knights on the two spaces in front of the test Knight to check that the
        # test Knight is able to jump over them, i.e. their presence along the Knight's movement
        # path do not prevent the Knight from legally making the move, and that the
        # pieces along the path remain where they were after the Knight is done with its move.

        current_space = test_white_knight.current_space
        ahead = test_board.get_space(current_space.file, current_space.rank + 1)
        two_ahead = test_board.get_space(current_space.file, current_space.rank + 2)
        target = test_board.get_space(chr(ord(current_space.file) + 1), current_space.rank + 2)

        first_obstacle_knight = Knight(PieceColor.WHITE)
        first_obstacle_knight.place(ahead)
        second_obstacle_knight = Knight(PieceColor.BLACK)
        second_obstacle_knight.place(two_ahead)

        test_white_knight.move(target)
        assert test_white_knight.current_space is target
        assert first_obstacle_knight.current_space is ahead
        assert second_obstacle_knight.current_space is two_ahead


class TestKnightCapture:

    # Test that the Knight can capture by moving two Spaces straight in one direction and one Space perpendicular.
    def test_knight_capture_up_right(self, test_board, test_white_knight, test_black_knight):
        assert test_board
        assert test_white_knight
        assert test_black_knight
        assert test_white_knight.current_space
        assert test_white_knight.current_space.rank + 2 <= MAX_RANK
        assert ord(test_white_knight.current_space.file) + 1 <= ord(MAX_FILE)

        target_file = chr(ord(test_white_knight.current_space.file) + 1)
        target_rank = test_white_knight.current_space.rank + 2
        target_space = test_board.get_space(target_file, target_rank)

        test_black_knight.place(target_space)

        test_white_knight.capture(target_space)
        assert test_white_knight.current_space is target_space
        assert not test_black_knight.current_space

    def bad_knight_capture(self, test_board, test_white_knight, test_black_knight):
        assert test_board
        assert test_white_knight
        assert test_black_knight
        assert test_black_knight.current_space

        test_white_knight.capture(test_black_knight.current_space)

    def test_bad_knight_capture(self, test_board, test_white_knight, test_black_knight):
        with pytest.raises(IllegalMoveException) as info:
            self.bad_knight_capture(test_board, test_white_knight, test_black_knight)
        assert "A Knight must capture two spaces straight and one space perpendicular." in str(info)