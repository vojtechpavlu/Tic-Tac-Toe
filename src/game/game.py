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

        # Kontrola, že jsou dodaní hráči validní. Pokud by nebyli,
        # byla by vyhozena výjimka
        self.__check_players()

    @property
    def players(self) -> tuple[Player]:
        """"""
        return tuple(self.__players)

    @property
    def player_names(self) -> tuple[str]:
        """"""
        return tuple([player.player_name for player in self.players])

    @property
    def player_marks(self) -> tuple[str]:
        """"""
        return tuple([player.mark for player in self.players])

    def __check_players(self):
        """Kontrola validity hráčů. Kontroluje se následující:

            - Počet hráčů - musí být právě dva hráči
            - Značky, kterými hráči označují svá políčka - musí být unikátní
        """
        # Pokud je počet hráčů jiný než 2
        if len(self.players) != 2:
            raise GameError(f"Počet hráčů musí být 2: {len(self.players)}")

        # Pokud je počet unikátních značek jiný, než počet hráčů
        elif len(set(self.player_marks)) != len(self.players):
            raise GameError(
                f"Každý hráč musí mít unikátní značku: {self.player_marks}")


class GameError(Exception):
    pass




