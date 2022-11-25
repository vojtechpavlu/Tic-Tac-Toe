""""""
from src.game.board import BoardSnapshot
from src.game.player import Player


class CustomPlayer(Player):
    """"""

    def __init__(self, player_name: str, mark: str):
        """"""
        Player.__init__(self, player_name, mark)

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """"""
        return valid_moves[0]






