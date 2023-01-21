"""Tento modul obsahuje racionálního hráče postaveného na algoritmu Minmax.
Cílem tohoto hráče je demonstrovat hledání optimální strategie.
"""

from src.game.board import BoardSnapshot
from src.game.player import Player


class MinmaxPlayer(Player):
    """Instance této třídy jsou odpovědné za simulaci neporazitelného hráče.
    Tento hráč je navržen tak, aby volil své tahy (své strategie) na základě
    garančního algoritmu minmax, čímž dosahuje v tom nejméně příznivém případě
    remízy.
    """

    # Distribuce výplat pro jednotlivé výsledky hry; slovník je inicializován
    # z initoru instance této třídy v závislosti na přiřazené značce
    __POINTS = {}

    def __init__(self, player_name: str, mark: str):
        """Initor instance, který přijímá v parametru název hráče a značku,
        kterou má používat pro označování svých políček.
        """
        # Volání initoru předka
        super().__init__(player_name, mark)

        # Inicializace slovníku výplat
        MinmaxPlayer.__POINTS = {
            mark: 1,                 # Body za výhru
            self.opponent_mark: -1,  # Body za prohru
            "draw": 0                # Bory za remízu
        }

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """"""
        new_board = self.__translate_board(board)
        return minimax(new_board, True, self.mark, self.opponent_mark)[1]

    @classmethod
    def points(cls):
        """"""
        return cls.__POINTS

    @staticmethod
    def __translate_board(board: BoardSnapshot) -> list[list[str]]:
        """Statická metoda odpovědná za převedení hrací plochy v podobě
        instance třídy `BoardSnapshot` do dvoudimenzionálního seznamu
        textových řetězců.
        """
        new_board = []
        base = board.board_base
        for y in range(base):
            new_board.append(
                [board.find_closure(x, y).mark for x in range(base)]
            )
        return new_board


def minimax(board, is_max, ai_mark, opp_mark) -> tuple[int, str]:
    """"""

    result = evaluate(board)

    if result:
        return MinmaxPlayer.points()[result], ""

    best_move = ""
    best_score = float("-inf") if is_max else float("inf")

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == "":
                board[y][x] = ai_mark if is_max else opp_mark
                score = minimax(board, not is_max, ai_mark, opp_mark)[0]
                board[y][x] = ""
                if is_max and score > best_score:
                    best_score = score
                    best_move = f"{x} {y}"
                elif not is_max and score < best_score:
                    best_score = score
                    best_move = f"{x} {y}"

    return best_score, best_move


def evaluate(board) -> str:
    """"""
    return (check_horizontals(board) or check_verticals(board) or
            check_diagonals(board) or check_draw(board))


def check_horizontals(board):
    """"""
    for line in board:
        if len(set(line)) == 1:
            return line[0]


def check_verticals(board):
    """"""
    for x in range(len(board[0])):
        line = []
        for y in range(len(board)):
            line.append(board[y][x])
        if len(set(line)) == 1:
            return line[0]


def check_diagonals(board):
    """"""
    first_diagonal = []
    second_diagonal = []
    for i in range(len(board)):
        first_diagonal.append(board[i][i])
        second_diagonal.append(board[len(board) - i - 1][i])
    if len(set(first_diagonal)) == 1:
        return first_diagonal[0]
    if len(set(second_diagonal)) == 1:
        return second_diagonal[0]


def check_draw(board):
    for y in range(len(board)):
        for x in range(len(board)):
            if not board[y][x]:
                return
    return "draw"













