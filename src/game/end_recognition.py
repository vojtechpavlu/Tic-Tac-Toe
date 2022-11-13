""""""


from abc import ABC, abstractmethod
from typing import Iterable

from src.game.board import BoardSnapshot
from src.game.field import FieldClosure
from src.game.game_resul_exceptions import Win, Draw


class EndRecognizer(ABC):
    """"""

    def __init__(self, description: str):
        self._desc = description

    @property
    def description(self) -> str:
        return self._desc

    @abstractmethod
    def is_end(self, board_snapshot: BoardSnapshot):
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
        EndRecognizer.__init__(
            self, f"Hráč spojil políčka v {column_number + 1}. sloupci.")
        self._column_number = column_number

    @property
    def column_number(self) -> int:
        """"""
        return self._column_number

    def is_end(self, board_snapshot: BoardSnapshot):
        """"""
        closures = board_snapshot.field_closures
        characters = []

        for y in range(3):
            characters.append(
                self.find_closure(self.column_number, y, closures).character)

        for character in characters:
            if character != characters[0]:
                break
        else:
            raise Win()


class Row(EndRecognizer):
    """"""

    def __init__(self, row_number: int):
        """"""
        EndRecognizer.__init__(
            self, f"Hráč spojil políčka v {row_number + 1}. řádku.")
        self._row_number = row_number

    @property
    def row_number(self) -> int:
        """"""
        return self._row_number

    def is_end(self, board_snapshot: BoardSnapshot):
        """"""
        closures = board_snapshot.field_closures
        characters = []

        for x in range(3):
            characters.append(
                self.find_closure(x, self.row_number, closures).character)

        for character in characters:
            if character != characters[0]:
                break
        else:
            raise Win()


class NoMoreMoves(EndRecognizer):
    """"""

    def __init__(self):
        EndRecognizer.__init__(self, "Již není žádný další možný tah.")

    def is_end(self, board_snapshot: BoardSnapshot):
        """"""
        if len(board_snapshot.valid_moves) == 0:
            raise Draw()
















