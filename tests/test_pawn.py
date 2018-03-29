"""
Tests for the Pawn class to ensure correct
placement, movement, capturing, and promotion
behavior, as well as correct attributes upon creation.

Last modified: 3/29/2018
Author: Daniel Edades
"""

import sys
import pytest
sys.path.append("..")
from board import Board
from pawn import Pawn
from piece import PieceColor
from piece import IllegalPlacementException
from piece import IllegalMoveException

MIN_RANK = 1
MAX_RANK = 8


@pytest.fixture
def test_board():
    test_board = Board()
    assert test_board

    return test_board


@pytest.fixture
def test_pawn(test_board):
    assert test_board

    starting_space = test_board.get_space("e", 2)
    test_pawn = Pawn(PieceColor.WHITE)

    test_pawn.place(starting_space)

    assert test_pawn
    assert test_pawn.current_space == starting_space

    return test_pawn


@pytest.fixture
def opposing_pawn(test_pawn):
    assert test_board

    opposing_pawn = Pawn(-(test_pawn.color.value))
    assert opposing_pawn
    return opposing_pawn


@pytest.fixture
def same_side_pawn(test_pawn):
    assert test_board

    same_side_pawn = Pawn(test_pawn.color)
    assert same_side_pawn
    return same_side_pawn


class TestPawn:

    # Placement Tests

    def test_place_pawn(self, test_board):
        """
        Explicitly tests the place() method without relying on the
        test_pawn fixture.
        """

        # Check that the intended Space is on the Board with the expected attributes.
        expected_file = "e"
        expected_rank = 2
        expected_name = expected_file + str(expected_rank)

        target_space = test_board.get_space(expected_file, expected_rank)

        assert target_space
        assert target_space.file == "e"
        assert target_space.rank == 2
        assert target_space.name == "e2"

        # Place a Pawn on the intended Space
        expected_color = PieceColor.WHITE
        test_pawn = Pawn(expected_color)

        # Check that the Pawn was created
        assert test_pawn

        test_pawn.place(target_space)

        # Check that the Pawn is on the intended Space
        assert test_pawn.current_space is target_space
        assert test_pawn.moved is False

    def place_bad_space(self, test_pawn):
        bad_space = None
        test_pawn.place(bad_space)

    def test_place_bad_space(self, test_pawn):
        with pytest.raises(IllegalPlacementException) as info:
            self.place_bad_space(test_pawn)
        assert "The target is not a Space." in str(info)

    # Movement Tests

    def test_move_pawn(self, test_board, test_pawn):

        assert test_board
        assert test_pawn

        starting_space = test_pawn.current_space
        starting_rank = starting_space.rank
        starting_file = starting_space.file

        # Move the Pawn two spaces forward
        first_move_space = test_board.get_space(starting_file, starting_rank + 2)
        assert first_move_space
        test_pawn.move(test_board, first_move_space)

        # Check that the Pawn is on the expected space
        current_space = test_pawn.current_space
        assert current_space.rank == starting_rank + 2
        assert current_space.file == starting_file

        # Check that the Pawn is treated as having moved
        assert test_pawn.moved is True

        # Move the pawn one space forward
        second_move_space = test_board.get_space(starting_file, starting_rank + 3)
        assert second_move_space
        test_pawn.move(test_board, second_move_space)

        # Check that the Pawn is on the expected space
        current_space = test_pawn.current_space
        assert current_space.rank == starting_rank + 3
        assert current_space.file == starting_file

    def move_two_spaces_twice(self, test_board, test_pawn):

        assert test_board
        assert test_pawn

        # Move the Pawn two spaces

        starting_space = test_pawn.current_space
        target_file = starting_space.file
        target_rank = starting_space.rank + 2
        target_space = test_board.get_space(target_file, target_rank)

        test_pawn.move(test_board, target_space)

        # Check that the Pawn cannot move two more spaces
        illegal_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 2)
        test_pawn.move(test_board, illegal_space)

    def test_enforce_one_square(self, test_board, test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_two_spaces_twice(test_board, test_pawn)
        assert "A Pawn may only move two Spaces on its first move." in str(info)

    def move_different_file(self, test_board, test_pawn):

        assert test_board
        assert test_pawn

        starting_space = test_pawn.current_space
        target_file = chr(ord(starting_space.file) + 1)
        illegal_space = test_board.get_space(target_file, starting_space.rank + 1)

        # Check that the Pawn cannot go to a different file with an ordinary move
        test_pawn.move(test_board, illegal_space)

    def test_enforce_move_same_file(self, test_board, test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_different_file(test_board, test_pawn)
        assert "A Pawn may not move to a different file unless capturing." in str(info)

    def move_too_many_squares(self, test_board, test_pawn, num_moves):

        assert test_board
        assert test_pawn
        assert isinstance(num_moves, int)

        starting_space = test_pawn.current_space
        target_file = starting_space.file

        # Check that the Pawn cannot move more than two spaces.
        target_rank = starting_space.rank + num_moves
        target_space = test_board.get_space(target_file, target_rank)
        test_pawn.move(test_board, target_space)

    def test_enforce_max_move_length(self, test_board, test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            for moves in range(3, 7):
                self.move_too_many_squares(test_board, test_pawn, moves)
        assert "A Pawn may never move more than two Spaces at a time." in str(info)

    def move_onto_occupied_square(self, test_board, test_pawn, occupying_pawn):

        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank < MAX_RANK
        assert occupying_pawn

        # Place a piece directly in front of the test Pawn
        occupying_pawn_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 1)
        occupying_pawn.place(occupying_pawn_space)

        # Try to move the test Pawn into the space of the other piece
        target_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 1)
        test_pawn.move(test_board, target_space)

    def test_enforce_no_move_into_occupied_by_opponent(self, test_board, test_pawn, opposing_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_onto_occupied_square(test_board, test_pawn, opposing_pawn)
        assert "Target space not empty." in str(info)

    def test_enforce_no_move_into_occupied_by_same(self, test_board, test_pawn, same_side_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_onto_occupied_square(test_board, test_pawn, same_side_pawn)
        assert "Target space not empty." in str(info)

    def move_over_occupied_square(self, test_board, test_pawn, occupying_pawn):

        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank < MAX_RANK - 1
        assert occupying_pawn

        # Place a piece two squares in front of the test Pawn
        occupying_pawn_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 1)
        occupying_pawn.place(occupying_pawn_space)

        # Try to move the test Pawn into the space behind the other piece
        target_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 2)
        test_pawn.move(test_board, target_space)

    def test_enforce_no_move_over_opponent_occupied(self, test_board, test_pawn, opposing_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_over_occupied_square(test_board, test_pawn, opposing_pawn)
        assert "may not jump" in str(info)

    def test_enforce_no_move_over_same_occupied(self, test_board, test_pawn, same_side_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_over_occupied_square(test_board, test_pawn, same_side_pawn)
        assert "may not jump" in str(info)


    def move_backward_white(self, test_board, test_pawn):

        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank > MIN_RANK

        #  Try to move the test Pawn backward one Space
        target_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank - 1)
        test_pawn.move(test_board, target_space)

    def test_enforce_no_backward_move_white(self, test_board, test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_backward_white(test_board, test_pawn)
        assert "not move backward" in str(info)

    def move_backward_black(self, test_board, test_pawn):

        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank < MAX_RANK
        test_pawn.color = PieceColor.BLACK

        # Try to move the test Pawn backward one Space
        target_space = test_board.get_space(test_pawn.current_space.file, test_pawn.current_space.rank + 1)
        test_pawn.move(test_board, target_space)

    def test_enforce_no_backward_move_black(self, test_board, test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_backward_black(test_board, test_pawn)
        assert "not move backward" in str(info)

    # Capturing Tests

    def test_capture_opposing_piece_left(self, test_board, test_pawn, opposing_pawn):
        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank < MAX_RANK
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the left of the test Pawn
        target_file = chr(ord(test_pawn.current_space.file) - 1)
        target_rank = test_pawn.current_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        test_pawn.capture(test_board, target_space)

        # Check that the test Pawn is now in the opposing Pawn's space
        assert test_pawn.current_space is target_space

        # Check that the opposing Pawn is off the board
        assert opposing_pawn.current_space is None

        # Check that the test Pawn is its Space's current piece
        assert target_space.current_piece is test_pawn

    def test_capture_opposing_piece_right(self, test_board, test_pawn, opposing_pawn):
        assert test_board
        assert test_pawn
        assert test_pawn.current_space.rank < MAX_RANK
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the right of the test Pawn
        target_file = chr(ord(test_pawn.current_space.file) + 1)
        target_rank = test_pawn.current_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        test_pawn.capture(test_board, target_space)

        # Check that the test Pawn is on the opposing Pawn's previous Space
        assert test_pawn.current_space is target_space

        # Check that the opposing Pawn has been removed from the board
        assert opposing_pawn.current_space is None

        # Check that the test Pawn is its Space's current piece
        assert target_space.current_piece is test_pawn

    def test_capture_test_pawn_left(self, test_board, test_pawn, opposing_pawn):
        assert test_board
        assert test_pawn
        assert opposing_pawn

        capture_space = test_pawn.current_space

        # Place the opposing Pawn one space in front of and one space to the left of the test Pawn
        target_file = chr(ord(test_pawn.current_space.file) - 1)
        target_rank = test_pawn.current_space.rank - 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the test pawn with the opposing Pawn
        opposing_pawn.capture(test_board, test_pawn.current_space)

        # Check that the opposing Pawn is on the test Pawn's previous Space
        assert opposing_pawn.current_space is capture_space

        # Check that the test Pawn is off the board
        assert test_pawn.current_space is None

        # Check that the opposing Pawn is its Space's current peice
        assert capture_space.current_piece is opposing_pawn


'''
    def test_enforce_only_capture_one_away(self):
        pass

    def test_enforce_no_backward_capture(self):
        pass

    def test_enforce_no_same_side_capture(self):
        pass
'''