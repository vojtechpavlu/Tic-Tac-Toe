""""""

from typing import Iterable
from src.game.field import Field


class Board:
    """"""

    def __init__(self, fields: Iterable[Field]):
        self._fields = list(fields)

    @property
    def fields(self) -> tuple[Field]:
        """Ntice políček, ze kterých se hrací plocha skládá."""
        return tuple(self._fields)

    @property
    def size(self) -> int:
        """Velikost hrací plochy coby počet políček."""
        return len(self.fields)

    @property
    def marked_fields(self) -> tuple[Field]:
        """Vrací ntici označených políček."""
        return tuple([field for field in self.fields if field.is_marked])

    @property
    def unmarked_fields(self) -> tuple[Field]:
        """Vrací ntici označených políček."""
        return tuple([field for field in self.fields if not field.is_marked])

    def has_field(self, x: int, y: int) -> bool:
        """Vrátí informaci o tom, zda-li je na hrací ploše políčko přítomné.
        """
        return self.field(x, y) is not None

    def field(self, x: int, y: int) -> Field:
        """Pokusí se najít políčko o daných souřadnicích a vrátí ho. Pokud
        takové políčko nalezeno není, je vráceno None.
        """
        for field in self.fields:
            if field.x == x and field.y == y:
                return field

    def mark(self, x: int, y: int, mark: str):
        """Pokusí se vyhledat políčko dle dodaných souřadnic a označit ho.
        Pokud takové políčko nebude nalezeno, je vyhozena výjimka.
        """
        field = self.field(x, y)
        if not field:
            raise BoardError(f"Políčko [{x}, {y}] nebylo nalezeno!", self)
        field.mark = mark


class BoardError(Exception):
    """"""

    def __init__(self, message: str, board: Board):
        Exception.__init__(self, message)
        self._board = board

    @property
    def board(self) -> Board:
        """Hrací plocha, v jejímž kontextu došlo k chybě."""
        return self._board




