from src.game.player import Player


class DummyPlayer(Player):

    def move(self) -> str:
        return "test_move"