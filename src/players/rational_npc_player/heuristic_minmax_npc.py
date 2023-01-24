""""""

from typing import Iterable
from src.game.board import BoardSnapshot
from src.game.player import Player
from src.players.rational_npc_player.evaluators import Evaluator
from src.players.rational_npc_player.utils import is_terminate, translate_board


class LimitedMinmaxPlayer(Player):
    """"""

    def __init__(self, player_name: str, mark: str, evaluators: Iterable[Evaluator] = (), max_depth: int = 9):
        super().__init__(player_name, mark)
        self.__max_depth = max_depth
        self.__evaluators: list[Evaluator] = list(evaluators)

    @property
    def max_depth(self) -> int:
        """"""
        return self.__max_depth

    @property
    def evaluators(self) -> tuple[Evaluator]:
        """"""
        return tuple(self.__evaluators)

    def add_evaluator(self, new_evaluator: Evaluator):
        """"""
        self.__evaluators.append(new_evaluator)

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """"""
        new_board = translate_board(board)
        return self.limited_minmax(
            new_board, True, self.max_depth)[1]

    def limited_minmax(self, board: list[list[str]], is_maximizing: bool,
                       depth: int) -> tuple[float, str]:
        """"""
        if depth == 0 or is_terminate(board):
            return self.evaluate(board), ""

        best_move = ""
        best_score = float("-inf") if is_maximizing else float("inf")
        current_mark = self.mark if is_maximizing else self.opponent_mark

        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == "":
                    board[y][x] = current_mark
                    score_for_move = self.limited_minmax(
                        board,
                        not is_maximizing,
                        depth - 1
                    )[0]

                    if is_maximizing and score_for_move > best_score:
                        best_score = score_for_move
                        best_move = f"{x} {y}"
                    elif not is_maximizing and score_for_move < best_score:
                        best_score = score_for_move
                        best_move = f"{x} {y}"

                    board[y][x] = ""
        return best_score, best_move

    def evaluate(self, board: list[list[str]]) -> float:
        """"""
        return sum([
            ef.evaluate(board, self.mark, self.opponent_mark)
            for ef in self.evaluators
        ])






