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

    result = is_terminate(board)

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


def is_terminate(board) -> str:
    """Funkce odpovědná za ověření, zda-li není stav (hrací plocha) již listem
    stromu (terminální uzel). Pokud ano, vrací značku výherce nebo textový
    řetězec `draw`. V opačném případě vrací prázdný řetězec.
    """
    return (check_horizontals(board) or check_verticals(board) or
            check_diagonals(board) or check_draw(board) or "")


def check_horizontals(board):
    """Funkce odpovědná za kontrolu řádků. Pokud jsou v některém z řádků
    vyplněna všechna políčka jedním hráčem, vrací funkce značku tohoto
    hráče, jinak vrací prázdný řetězec.
    """
    for line in board:
        if len(set(line)) == 1:
            return line[0]
    return ""


def check_verticals(board):
    """Funkce odpovědná za kontrolu, zda-li není zcela vyplněn některý ze
    sloupečků hrací plochy značkami jednoho hráče. Pokud ano, vrací jeho
    značku, jinak prázdný řetězec.
    """
    for x in range(len(board[0])):
        line = []
        for y in range(len(board)):
            line.append(board[y][x])
        if len(set(line)) == 1:
            return line[0]
    return ""


def check_diagonals(board):
    """Funkce odpovědná za provedení kontroly obou diagonál. Pokud je alespoň
    jedna diagonála vyplněna stejnou značkou, vrací tuto značku. Jinak vrací
    prázdný řetězec.
    """
    first_diagonal = []
    second_diagonal = []
    for i in range(len(board)):
        first_diagonal.append(board[i][i])
        second_diagonal.append(board[len(board) - i - 1][i])
    if len(set(first_diagonal)) == 1:
        return first_diagonal[0]
    elif len(set(second_diagonal)) == 1:
        return second_diagonal[0]
    else:
        return ""


def check_draw(board) -> str:
    """Funkce odpovědná za kontrolu, že hra dospěla, resp. nedospěla do
    remízového stavu. Pokud najde volné políčko, které lze vyplnit, funkce
    vrací prázdný řetězec; pokud takové políčko neexistuje, vrací textový
    řetězec `draw`.
    """
    for y in range(len(board)):
        for x in range(len(board)):
            if not board[y][x]:
                return ""
    return "draw"













