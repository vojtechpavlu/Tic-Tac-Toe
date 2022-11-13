""""""

from src.game.player import Player
from src.game.board import BoardSnapshot


class HumanPlayer(Player):
    """"""

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """"""
        print(board.stringify)
        print(valid_moves)
        return input("Zadej svůj tah: ")





