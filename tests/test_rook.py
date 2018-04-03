"""
Tests for the Rook class to ensure correct
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

