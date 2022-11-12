""""""


from abc import ABC, abstractmethod


class Player(ABC):
    """"""

    __AVAILABLE_MARKS = ("X", "O")

    def __init__(self, player_name: str, mark: str):
        """"""
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
    def mark(self) -> str:
        """Značka, kterou hráč označuje políčko svého tahu."""
        return self.__mark

    @abstractmethod
    def move(self) -> str:
        """Abstraktní metoda reprezentující tah hráče. Tah hráč zadává coby
        textovou reprezentaci."""

    @classmethod
    def available_marks(cls) -> tuple[str, str]:
        """Povolené značky, kterými může hráč označit své políčko."""
        return Player.__AVAILABLE_MARKS


class PlayerError(Exception):
    """"""

    def __init__(self, message: str, player: Player):
        """"""
        Exception.__init__(self, message)
        self._player = player

    @property
    def player(self) -> Player:
        """"""
        return self._player

