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
            "draw": 0                # Body za remízu
        }

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Metoda odpovědná za výběr optimálního, leč racionálního tahu.
        Přijímá otisk hrací plochy, který si převádí do interní reprezentace
        pomocí privátní statické metody
        `__translate_board(BoardSnapshot) -> list[list[str]]`. Tento proces
        byl zvolen jako výpočetně nejpoužitelnější.

        Dále tato metoda iniciuje minimax algoritmus, který vrací zvolený tah.
        """
        new_board = self.__translate_board(board)
        return minimax(new_board, True, self.mark, self.opponent_mark)[1]

    @classmethod
    def points(cls):
        """Třídní metoda vracející bodové ohodnocení pro jednotlivé výsledky.
        """
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


def minimax(board: list[list[str]], is_maximizing: bool, minmax_mark: str,
            opponent_mark: str) -> tuple[int, str]:
    """Samotná definice rekurzivního garančního algoritmu minmax, který
    je odpovědný za výběr tahu s největším potenciálem na výhru.

    Funkce vrací bodový zisk a tah, který k němu vede.
    """

    # Test terminality uzlu - uloží si výsledek
    result = is_terminate(board)

    # Pokud je terminální (výsledek jiný než prázdný řetězec)
    if result:
        return MinmaxPlayer.points()[result], ""

    # Připrav si aktuální odhady nejlepšího tahu a nejlepšího výsledku
    best_move = ""
    best_score = float("-inf") if is_maximizing else float("inf")

    # Pro každé políčko
    for y in range(len(board)):
        for x in range(len(board)):

            # Lze-li políčko vyplnit
            if board[y][x] == "":

                # Nastav políčku značku aktuálního hráče
                board[y][x] = minmax_mark if is_maximizing else opponent_mark

                # Zjisti aktuální skóre rekurzivním zavoláním sebe sama
                score = minimax(
                    board,
                    not is_maximizing,
                    minmax_mark,
                    opponent_mark
                )[0]

                # Pokud je skóre pro daného hráče výhodné, je to pro něj
                # doposud nejlepší tah
                if is_maximizing and score > best_score:
                    best_score = score
                    best_move = f"{x} {y}"
                elif not is_maximizing and score < best_score:
                    best_score = score
                    best_move = f"{x} {y}"

                # V rámci backtrackingu se vrať
                board[y][x] = ""

    # Vrať nejlepší nalezené skóre při aplikaci vráceného tahu
    return best_score, best_move


def is_terminate(board: list[list[str]]) -> str:
    """Funkce odpovědná za ověření, zda-li není stav (hrací plocha) již listem
    stromu (terminální uzel). Pokud ano, vrací značku výherce nebo textový
    řetězec `draw`. V opačném případě vrací prázdný řetězec.
    """
    return (check_horizontals(board) or check_verticals(board) or
            check_diagonals(board) or check_draw(board) or "")


def check_horizontals(board: list[list[str]]) -> str:
    """Funkce odpovědná za kontrolu řádků. Pokud jsou v některém z řádků
    vyplněna všechna políčka jedním hráčem, vrací funkce značku tohoto
    hráče, jinak vrací prázdný řetězec.
    """
    for line in board:
        if len(set(line)) == 1:
            return line[0]
    return ""


def check_verticals(board: list[list[str]]) -> str:
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


def check_diagonals(board: list[list[str]]) -> str:
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


def check_draw(board: list[list[str]]) -> str:
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













