"""Jednoduchý modul coby přístupový bod pro vlastní implementace automatického
hráče.
"""

from src.game.board import BoardSnapshot
from src.game.player import Player


class CustomPlayer(Player):
    """Šablona hráče pro studenty."""

    def __init__(self, player_name: str, mark: str):
        """Jednoduchý initor"""
        Player.__init__(self, player_name, mark)

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Obecná metoda, která je třeba pro implementaci."""
        return valid_moves[0]






