from piece import *
from board import *
from enum import Enum


class Knight(Piece):

    def __init__(self, color):
        super().__init__(color)