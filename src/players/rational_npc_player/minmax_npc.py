"""Tento modul obsahuje racionálního hráče postaveného na algoritmu Minmax.
Cílem tohoto hráče je demonstrovat hledání optimální strategie.
"""

from src.game.board import BoardSnapshot
from src.game.player import Player
from src.players.rational_npc_player.utils import is_terminate, translate_board


class MinmaxNPC(Player):
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
        MinmaxNPC.__POINTS = {
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
        new_board = translate_board(board)
        return minimax(new_board, True, self.mark, self.opponent_mark)[1]

    @classmethod
    def points(cls):
        """Třídní metoda vracející bodové ohodnocení pro jednotlivé výsledky.
        """
        return cls.__POINTS


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
        return MinmaxNPC.points()[result], ""

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














