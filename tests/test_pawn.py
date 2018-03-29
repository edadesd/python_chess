"""
Tests for the Pawn class to ensure correct
placement, movement, capturing, and promotion
behavior, as well as correct attributes upon creation.

Last modified: 3/29/2018
Author: Daniel Edades
"""

import sys
import pytest
import random
sys.path.append("..")
from board import Board
from pawn import Pawn
from piece import PieceColor
from piece import IllegalPlacementException
from piece import IllegalMoveException

MIN_RANK = 1
MAX_RANK = 8
RANKS = (1, 2, 3, 4, 5, 6, 7, 8)
FILES = ("a", "b", "c", "d", "e", "f", "g", "h")

@pytest.fixture
def test_board():
    test_board = Board()
    assert test_board

    return test_board


@pytest.fixture
def white_test_pawn(test_board):
    assert test_board

    starting_space = test_board.get_space("e", 2)
    test_pawn = Pawn(PieceColor.WHITE)

    test_pawn.place(starting_space)

    assert test_pawn
    assert test_pawn.current_space == starting_space

    return test_pawn

@pytest.fixture
def black_test_pawn(test_board):
    assert test_board

    starting_space = test_board.get_space("e", 7)
    test_pawn = Pawn(PieceColor.BLACK)

    test_pawn.place(starting_space)

    assert test_pawn
    assert test_pawn.current_space == starting_space

    return test_pawn


# Placement Tests
class TestPawnPlace:

    def test_place_pawn(self, test_board):
        """
        Explicitly tests the place() method without relying on the
        test_pawn fixture.
        """

        # Check that the intended Space is on the Board with the expected attributes.
        expected_file = random.choice(FILES)
        expected_rank = random.choice(RANKS)
        expected_name = expected_file + str(expected_rank)

        target_space = test_board.get_space(expected_file, expected_rank)

        assert target_space
        assert target_space.file == expected_file
        assert target_space.rank == expected_rank
        assert target_space.name == expected_name

        # Place a Pawn on the intended Space
        expected_color = PieceColor.WHITE
        test_pawn = Pawn(expected_color)

        # Check that the Pawn was created
        assert test_pawn

        test_pawn.place(target_space)

        # Check that the Pawn is on the intended Space
        assert test_pawn.current_space is target_space
        assert test_pawn.moved is False

    def place_bad_space(self, white_test_pawn):
        bad_space = None
        white_test_pawn.place(bad_space)

    def test_place_bad_space(self, white_test_pawn):
        with pytest.raises(IllegalPlacementException) as info:
            self.place_bad_space(white_test_pawn)
        assert "The target is not a Space." in str(info)

# Removal Tests
class TestRemovePawn:

    def test_remove_pawn(self, test_board, white_test_pawn):
        assert white_test_pawn
        assert white_test_pawn.current_space

        original_space = white_test_pawn.current_space
        white_test_pawn.remove()

        assert not white_test_pawn.current_space
        assert not original_space.current_piece



# Movement Tests
class TestPawnMove:

    def test_move_pawn(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn
        assert white_test_pawn.color is PieceColor.WHITE

        starting_space = white_test_pawn.current_space
        starting_rank = starting_space.rank
        starting_file = starting_space.file

        # Move the Pawn two spaces forward
        first_move_space = test_board.get_space(starting_file, starting_rank + 2)
        assert first_move_space
        white_test_pawn.move(test_board, first_move_space)

        # Check that the Pawn is on the expected space
        current_space = white_test_pawn.current_space
        assert current_space.rank == starting_rank + 2
        assert current_space.file == starting_file

        # Check that the Pawn is treated as having moved
        assert white_test_pawn.moved is True

        # Move the pawn one space forward
        second_move_space = test_board.get_space(starting_file, starting_rank + 3)
        assert second_move_space
        white_test_pawn.move(test_board, second_move_space)

        # Check that the Pawn is on the expected space
        current_space = white_test_pawn.current_space
        assert current_space.rank == starting_rank + 3
        assert current_space.file == starting_file

    def move_two_spaces_twice(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn

        # Move the Pawn two spaces

        starting_space = white_test_pawn.current_space
        target_file = starting_space.file
        target_rank = starting_space.rank + 2
        target_space = test_board.get_space(target_file, target_rank)

        white_test_pawn.move(test_board, target_space)

        # Check that the Pawn cannot move two more spaces
        illegal_space = test_board.get_space(white_test_pawn.current_space.file, white_test_pawn.current_space.rank + 2)
        white_test_pawn.move(test_board, illegal_space)

    def test_enforce_one_square(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_two_spaces_twice(test_board, white_test_pawn)
        assert "A Pawn may only move two Spaces on its first move." in str(info)

    def move_different_file(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn

        starting_space = white_test_pawn.current_space
        target_file = chr(ord(starting_space.file) + 1)
        illegal_space = test_board.get_space(target_file, starting_space.rank + 1)

        # Check that the Pawn cannot go to a different file with an ordinary move
        white_test_pawn.move(test_board, illegal_space)

    def test_enforce_move_same_file(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_different_file(test_board, white_test_pawn)
        assert "A Pawn may not move to a different file unless capturing." in str(info)

    def move_too_many_squares(self, test_board, white_test_pawn, num_moves):

        assert test_board
        assert white_test_pawn
        assert isinstance(num_moves, int)

        starting_space = white_test_pawn.current_space
        target_file = starting_space.file

        # Check that the Pawn cannot move more than two spaces.
        target_rank = starting_space.rank + num_moves
        target_space = test_board.get_space(target_file, target_rank)
        white_test_pawn.move(test_board, target_space)

    def test_enforce_max_move_length(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            for moves in range(3, 7):
                self.move_too_many_squares(test_board, white_test_pawn, moves)
        assert "A Pawn may never move more than two Spaces at a time." in str(info)

    def move_onto_occupied_square(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn

        # Place a piece directly in front of the test Pawn
        occupying_pawn = Pawn(-(white_test_pawn.color.value))
        occupying_pawn_space = test_board.get_space(white_test_pawn.current_space.file,
                                                    white_test_pawn.current_space.rank + 1)
        occupying_pawn.place(occupying_pawn_space)

        # Try to move the test Pawn into the space of the other piece
        target_space = test_board.get_space(white_test_pawn.current_space.file, white_test_pawn.current_space.rank + 1)
        white_test_pawn.move(test_board, target_space)

    def test_enforce_no_move_into_occupied(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_onto_occupied_square(test_board, white_test_pawn)
        assert "Target space not empty." in str(info)

    def move_over_occupied_square(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn
        assert white_test_pawn.current_space.rank < MAX_RANK - 1

        occupying_pawn = Pawn(-(white_test_pawn.color.value))

        # Place a piece two squares in front of the test Pawn
        occupying_pawn_space = test_board.get_space(white_test_pawn.current_space.file,
                                                    white_test_pawn.current_space.rank + 1)
        occupying_pawn.place(occupying_pawn_space)

        # Try to move the test Pawn into the space behind the other piece
        target_space = test_board.get_space(white_test_pawn.current_space.file, white_test_pawn.current_space.rank + 2)
        white_test_pawn.move(test_board, target_space)

    def test_enforce_no_move_over_occupied(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_over_occupied_square(test_board, white_test_pawn)
        assert "A Pawn may not jump over any other piece" in str(info)

    def move_backward_white(self, test_board, white_test_pawn):

        assert test_board
        assert white_test_pawn
        assert white_test_pawn.current_space.rank > MIN_RANK

        #  Try to move the test Pawn backward one Space
        target_space = test_board.get_space(white_test_pawn.current_space.file, white_test_pawn.current_space.rank - 1)
        white_test_pawn.move(test_board, target_space)

    def test_enforce_no_backward_move_white(self, test_board, white_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_backward_white(test_board, white_test_pawn)
        assert "not move backward" in str(info)

    def move_backward_black(self, test_board, black_test_pawn):

        assert test_board
        assert black_test_pawn
        assert black_test_pawn.current_space.rank < MAX_RANK

        # Try to move the test Pawn backward one Space
        target_space = test_board.get_space(black_test_pawn.current_space.file, black_test_pawn.current_space.rank + 1)
        black_test_pawn.move(test_board, target_space)

    def test_enforce_no_backward_move_black(self, test_board, black_test_pawn):
        with pytest.raises(IllegalMoveException) as info:
            self.move_backward_black(test_board, black_test_pawn)
        assert "not move backward" in str(info)


# Capturing Tests
class TestPawnCapture:

    def test_white_capture_left(self, test_board, white_test_pawn):
        assert test_board
        assert white_test_pawn
        assert white_test_pawn.current_space.rank < MAX_RANK

        opposing_pawn = Pawn(-(white_test_pawn.color.value))
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the left of the test Pawn
        target_file = chr(ord(white_test_pawn.current_space.file) - 1)
        target_rank = white_test_pawn.current_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        white_test_pawn.capture(target_space)

        # Check that the test Pawn is now in the opposing Pawn's space
        assert white_test_pawn.current_space is target_space

        # Check that the opposing Pawn is off the board
        assert opposing_pawn.current_space is None

        # Check that the test Pawn is its Space's current piece
        assert target_space.current_piece is white_test_pawn

    def test_white_capture_right(self, test_board, white_test_pawn):
        assert test_board
        assert white_test_pawn
        assert white_test_pawn.current_space.rank < MAX_RANK

        opposing_pawn = Pawn(-(white_test_pawn.color.value))
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the right of the test Pawn
        target_file = chr(ord(white_test_pawn.current_space.file) + 1)
        target_rank = white_test_pawn.current_space.rank + 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        white_test_pawn.capture(target_space)

        # Check that the test Pawn is on the opposing Pawn's previous Space
        assert white_test_pawn.current_space is target_space

        # Check that the opposing Pawn has been removed from the board
        assert opposing_pawn.current_space is None

        # Check that the test Pawn is its Space's current piece
        assert target_space.current_piece is white_test_pawn

    def test_black_capture_left(self, test_board, black_test_pawn):
        assert test_board
        assert black_test_pawn

        opposing_pawn = Pawn(-(black_test_pawn.color.value))
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the left of the test Pawn
        target_file = chr(ord(black_test_pawn.current_space.file) - 1)
        target_rank = black_test_pawn.current_space.rank - 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        black_test_pawn.capture(target_space)

        # Check that the test Pawn is on the opposing Pawn's previous Space
        assert black_test_pawn.current_space is target_space

        # Check that the opposing Pawn has been removed from the board
        assert opposing_pawn.current_space is None

        # Check that the test Pawn is its Space's current piece
        assert target_space.current_piece is black_test_pawn

    def test_black_capture_right(self, test_board, black_test_pawn):
        assert test_board
        assert black_test_pawn

        opposing_pawn = Pawn(-(black_test_pawn.color.value))
        assert opposing_pawn

        # Place the opposing Pawn one space in front of and one space to the right of the test Pawn
        target_file = chr(ord(black_test_pawn.current_space.file) + 1)
        target_rank = black_test_pawn.current_space.rank - 1
        target_space = test_board.get_space(target_file, target_rank)
        opposing_pawn.place(target_space)

        # Capture the opposing Pawn with the test Pawn
        black_test_pawn.capture(target_space)

        # Check that the test Pawn is on the opposing Pawn's previous Space
        assert black_test_pawn.current_space is target_space

        # Check that the opposing Pawn has been removed from the board
        assert opposing_pawn.current_space is None

        # Check that the Pawn is its Space's current piece
        assert target_space.current_piece is black_test_pawn


'''
    def test_enforce_only_capture_one_away(self):
        pass

    def test_enforce_no_backward_capture_white(self):
        pass
        
    def test_enforce_no_backward_capture_black(self):
        pass

    def test_enforce_no_same_side_capture_white(self):
        pass
        
    def test_enforce_no_same_side_capture_black(self):
        pass
'''