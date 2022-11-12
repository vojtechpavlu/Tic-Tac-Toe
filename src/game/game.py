""""""

from typing import Iterable

from src.game.board import Board, default_board
from src.game.player import Player


class Game:
    """"""

    def __init__(self, players: Iterable[Player],
                 board: Board = default_board()):
        """"""
        self.__players = list(players)
        self.__board = board


class GameError(Exception):
    pass




