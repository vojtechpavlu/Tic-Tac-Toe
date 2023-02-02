"""Tento modul obsahuje definici heuristického racionálního hráče, který
vybírá své tahy na základě pomocných evaluačních funkcí.

Jeho síla oproti rigidnímu a rigoróznímu `MinmaxPlayer` je schopnost omezeného
prohledávání do hloubky, díky čemuž sice může obětovat absolutně nejlepší tah
na úkor zásadnímu zlepšení výkonu. Díky snížené hloubky prohledávání je pomocí
tohoto přístupu schopen částečně překračovat problém s komplexitou vícepolních
herních ploch.
"""

from typing import Iterable
from src.game.board import BoardSnapshot
from src.game.player import Player
from src.players.rational_npc_player.evaluators import Evaluator
from src.players.rational_npc_player.utils import is_terminate, translate_board


class LimitedMinmaxPlayer(Player):
    """Instance této třídy jsou odpovědné za racionální hraní hry piškvorky,
    přičemž uvažují jen omezený počet tahů.

    Toho dosahují pomocí množiny evaluátorů, které dokáží vyhodnotit kvalitu
    aktuálního snímku hrací plochy, díky čemuž může odhadovat bonitu svých
    rozhodování v 'reálném čase'.
    """

    def __init__(self, player_name: str, mark: str,
                 evaluators: Iterable[Evaluator] = (), max_depth: int = 9):
        """Initor, který přijímá hráčovo jméno, značku, kterou označuje svá
        políčka (tahy), iterovatelnou množinu evaluačních funkcí (instancí
        typu `Evaluator`), které budou použity pro vyhodnocování tahů, a
        hloubku maximálního prohledávání.

        Pro maximální hloubku prohledávání platí, že čim vyšší, tím
        kvalitnější tahy hráč hraje. Ovšem za cenu vyšší výpočetní složitosti,
        kterou musí při volbě tahu překonat.
        """
        super().__init__(player_name, mark)
        self.__max_depth = max_depth
        self.__evaluators: list[Evaluator] = list(evaluators)

    @property
    def max_depth(self) -> int:
        """Maximální hloubka, ve které bude algoritmus prohledávat."""
        return self.__max_depth

    @property
    def evaluators(self) -> tuple[Evaluator]:
        """Ntice evaluačních funkcí, které jsou při rozhodování použity."""
        return tuple(self.__evaluators)

    def add_evaluator(self, new_evaluator: Evaluator):
        """Funkce pro přidání nové evaluační funkce pro ohodnocování svých
        rozhodnutí."""
        self.__evaluators.append(new_evaluator)

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Funkce odpovědná za výběr následujícího tahu."""
        new_board = translate_board(board)
        return self.limited_minmax(
            new_board, True, self.max_depth)[1]

    def limited_minmax(self, board: list[list[str]], is_maximizing: bool,
                       depth: int) -> tuple[float, str]:
        """Metoda odpovědná za samotné vyhodnocení tahu co do bonity jeho
        následníků (listů).
        """
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






