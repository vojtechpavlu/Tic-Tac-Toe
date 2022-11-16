from src.game.board import default_board
from src.game.game import Game
from src.players.human_player.human_player import HumanPlayer

players = [HumanPlayer("H1", "X"), HumanPlayer("H2", "O")]

game = Game(players, default_board(4))

game.run_game()
