"""Tento modul obsahuje jednoduchou implementaci rozhraní pro lidského hráče,
který díky tomuto přístupu může interagovat s hrou.
"""

from src.game.player import Player
from src.game.board import BoardSnapshot


class HumanPlayer(Player):
    """Instance této třídy slouží jako rozhraní pro lidského hráče pro
    standardizaci interakce s hrou.

    Celý mechanismus tohoto rozhraní je postaven na přijímání uživatelských
    textových zpráv na požádání.
    """

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Jednoduchá implementace tahu hráče, který je chápán jako vyžádání
        si uživatelského textového vstupu pomocí built-in funkce `input`.

        Před tím je však uživateli jasně vyznačena hrací plocha a všechny
        validní kroky.
        """
        # Vypíše ukázku stavu hry a jeho možné validní tahy
        print(board.stringify, "\n")
        print("Možné tahy:", valid_moves, "\n")

        # Dotázání se na tah uživatele a jeho úvodní očištění od mezer
        # na počátku a na konci vstupního řetězce
        return input("Zadej svůj tah: ").strip()





