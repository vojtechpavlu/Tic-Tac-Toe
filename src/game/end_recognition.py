""""""


from abc import ABC, abstractmethod
from typing import Iterable

from src.game.board import BoardSnapshot
from src.game.field import FieldClosure


class EndRecognizer(ABC):
    """"""

    @abstractmethod
    def is_end(self, board_snapshot: BoardSnapshot) -> bool:
        """"""

    @staticmethod
    def find_closure(x: int, y: int, closures: Iterable[FieldClosure]):
        """"""
        for closure in closures:
            if closure.coords == (x, y):
                return closure
        raise Exception(
            f"Obálka políčka se souřadnicemi [{x}, {y}] nebyla nalezena")


class Column(EndRecognizer):
    """"""

    def __init__(self, column_number: int):
        """"""
        self._column_number = column_number

    @property
    def column_number(self) -> int:
        """"""
        return self._column_number

    def is_end(self, board_snapshot: BoardSnapshot) -> bool:
        """"""
        closures = board_snapshot.field_closures
        characters = []

        for y in range(3):
            characters.append(
                self.find_closure(self.column_number, y, closures).character)

        for character in characters:
            if character != characters[0]:
                return False
        return True


class NoMoreMoves(EndRecognizer):
    """"""

    def is_end(self, board_snapshot: BoardSnapshot) -> bool:
        """"""
        return len(board_snapshot.valid_moves) == 0
















