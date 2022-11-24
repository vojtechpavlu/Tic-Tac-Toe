"""Tento modul obsahuje definici náhodného hráče, resp. hráče vybárajícího
tahy zcela na základě náhody.

Tento způsob je uveden jen pro potřeby testování a demonstrace nevhodného
způsobu, neboť jeho rozhodování bude 'srovnatelné se šimpanzem'.
"""

import random

from src.game.board import BoardSnapshot
from src.game.player import Player


class RandomNPCPlayer(Player):
    """Instance této třídy reprezentují hráče, který hraje zcela náhodně, tedy
    své tahy ve hře vybírá zcela na základě náhody.
    """

    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Metoda zdědená z předka, která je odpovědná za provedení tahu ve
        hře. Metoda je postavena na podstatě výběru náhodného tahu ze sady
        všech přípustných tahů.
        """
        return random.choice(valid_moves)




