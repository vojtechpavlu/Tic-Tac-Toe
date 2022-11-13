"""Modul obsahuje všechny důležité prostředky pro práci s hrací plochou.

Konkrétně obsahuje definici třídy `Board` a definici specifické výjimky,
dojde-li k problému v rámci hrací plochy (`BoardError`).
"""

from typing import Iterable
from src.game.field import Field, FieldClosure


class Board:
    """Instance této třídy reprezentují hrací plochu a poskytují základní
    nástroje pro práci s ní.

    Samotná hrací plocha se sestává z políček (instancí třídy `Field`).
    """

    def __init__(self, fields: Iterable[Field]):
        """Initor, který přijímá iterovatelnou sadu všech políček, která
        mají danou hrací plochu reprezentovat.
        """
        self.__fields = list(fields)

        self.__check_fields()

    @property
    def fields(self) -> tuple[Field]:
        """Ntice políček, ze kterých se hrací plocha skládá."""
        return tuple(self.__fields)

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

    @property
    def __field_cords(self) -> tuple[tuple[int, int]]:
        """Vrací ntici dvojic (také ntic) reprezentujících souřadnice políček.
        """
        return tuple([field.xy for field in self.fields])

    @property
    def board_state(self) -> tuple[tuple[str]]:
        """"""
        lines = []
        substitutes = list(range(1, 10))
        for y in range(3):
            line = []
            for x in range(3):
                f = self.field(x, y)
                line.append(f.mark if f.is_marked else str(substitutes.pop(0)))
            lines.append(tuple(line))
        return tuple(lines)

    @property
    def copy(self) -> "Board":
        """Vrací hlubokou kopii tohoto objektu."""
        return Board([f.copy for f in self.fields])

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

    def __check_fields(self):
        """Metoda, která se stará o ověření správnosti hrací plochy.
        Kontroluje se přitom, zda všechna políčka mají unikátní souřadnice.
        """
        if len(set(self.__field_cords)) != self.size:
            raise BoardError(f"Souřadnice jednotlivých políček musí být "
                             f"unikátní: {self.__field_cords}", self)


class BoardSnapshot:
    """"""

    def __init__(self, board: Board):
        """"""
        self.__board = board.copy

    @property
    def fields(self) -> tuple[Field]:
        """"""
        return self.__board.fields

    @property
    def empty_fields(self) -> tuple[Field]:
        """"""
        return tuple([f for f in self.__board.fields if not f.is_marked])

    @property
    def played_fields(self) -> tuple[Field]:
        """"""
        return tuple([f for f in self.__board.fields if f.is_marked])

    @property
    def field_closures(self) -> tuple[FieldClosure]:
        """"""
        closures = []
        substitutes = list(range(1, 10))
        for y in range(3):
            for x in range(3):
                f = self.__board.field(x, y)
                mark = str(substitutes.pop(0)) if not f.is_marked else None
                closures.append(FieldClosure(f, mark))
        return tuple(closures)

    @property
    def valid_moves(self) -> tuple[FieldClosure]:
        """"""
        return tuple([fc for fc in self.field_closures
                      if fc.has_substitute_character])


def default_board() -> Board:
    """Tovární funkce pro vytvoření obecné, jednoduché hrací plochy s výchozím
    nastavením."""
    # Inicializace prázdného seznamu
    fields = []

    # Vygenerování všech políček
    for x in range(3):
        for y in range(3):
            fields.append(Field(x, y))

    # Navrácení nové instance hrací plochy
    return Board(fields)


class BoardError(Exception):
    """Výjimka rozšiřující obecnou třídu výjimky, která poskytuje specifické
    rozhraní pro poskytování hrací plochy, v jejímž kontextu došlo k chybě.
    """

    def __init__(self, message: str, board: Board):
        """Initor, který přijímá zprávu o chybě a hrací plochu, v jejímž
        kontextu k chybě došlo.
        """
        Exception.__init__(self, message)
        self._board = board

    @property
    def board(self) -> Board:
        """Hrací plocha, v jejímž kontextu došlo k chybě."""
        return self._board




