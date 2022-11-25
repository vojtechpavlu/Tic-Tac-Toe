from src.game.board import default_board
from src.game.game import Game
from src.players.human_player.human_player import HumanPlayer
from src.players.random_player.random_npc_player import RandomNPCPlayer

players = [HumanPlayer("H1", "X"), RandomNPCPlayer("H2", "O")]

game = Game(players, default_board(4))

game.run_game()
