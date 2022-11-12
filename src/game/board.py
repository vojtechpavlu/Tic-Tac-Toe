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






