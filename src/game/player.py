"""Modul obsahuje všechny prostředky pro definici hráče.

Konkrétně pak obsahuje především definici abstraktní třídy `Player`, která
slouží jako společný předek pro všechny typy hráčů - živých i NPC.
"""


from abc import ABC, abstractmethod
from src.game.board import BoardSnapshot


class Player(ABC):
    """Instance této abstraktní třídy umožňují sdružovat společný protokol
    pro všechny typy hráčů - pro 'živé' i pro tzv. NPC.

    Hráč je chápán jako entita schopná interagovat s hrou."""

    # Značky, kterými mohou hráči označovat svá políčka. Pokud by se pokusil
    # hráč používat jiných značek, je při iniciaci instance vyhozena výjimka
    __AVAILABLE_MARKS = ("X", "O")

    def __init__(self, player_name: str, mark: str):
        """Initor, který přijímá jméno hráče a značku, kterou bude používat
        pro označování svých políček.
        """
        self.__player_name = player_name
        self.__mark = mark

        if mark not in self.__AVAILABLE_MARKS:
            raise PlayerError(
                f"Neplatná značka hráče: '{mark}'. Použijte některou z "
                f"povolených: {self.__AVAILABLE_MARKS}", self)

        elif not player_name:
            raise PlayerError(
                f"Zadáno neplatné jméno hráče: {player_name}", self)

    @property
    def player_name(self) -> str:
        """Jméno hráče"""
        return self.__player_name

    @property
    def opponent_mark(self) -> str:
        """Značka, kterou používá protihráč."""
        return "X" if self.mark == "O" else "O"

    @property
    def mark(self) -> str:
        """Značka, kterou hráč označuje políčko svého tahu."""
        return self.__mark

    @abstractmethod
    def move(self, board: BoardSnapshot, valid_moves: tuple[str]) -> str:
        """Abstraktní metoda reprezentující tah hráče. Tah hráč zadává coby
        textovou reprezentaci."""

    @classmethod
    def available_marks(cls) -> tuple[str, str]:
        """Povolené značky, kterými může hráč označit své políčko."""
        return Player.__AVAILABLE_MARKS


class PlayerError(Exception):
    """Výjimka reprezentující chybu vzniklou v kontextu práce s instancí
    třídy `Player`. Ta na rozdíl od svého předka udržuje referenci na hráče,
    v jehož kontextu k chybě došlo. Díky tomu je možné lépe strojově reagovat
    na možné problémy."""

    def __init__(self, message: str, player: Player):
        """Initor, který přijímá kromě textové zprávy o chybě také referenci
        na hráče, v jehož kontextu k chybě došlo.
        """
        Exception.__init__(self, message)
        self._player = player

    @property
    def player(self) -> Player:
        """Instance třídy `Player`, v jejímž kontextu došlo k chybě."""
        return self._player

