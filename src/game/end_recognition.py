"""Tento modul obsahuje definice rozpoznavatelů konce hry.
"""


from abc import ABC, abstractmethod
from typing import Iterable

from src.game.board import BoardSnapshot
from src.game.field import FieldClosure
from src.game.game_resul_exceptions import Win, Draw


class EndRecognizer(ABC):
    """Obecný abstraktní předek všech zakončení hry.

    Stanovuje společný protokol pro všechny rozpoznavatele, především pak
    metodou `is_end(BoardSnapshot)`, pomocí které lze rozpoznat, zda-li je
    aktuální rozložení herní plochy cílové či nikoliv.
    """

    def __init__(self, description: str):
        """Initor, který přijímá textový popis zakončení."""
        self._desc = description

    @property
    def description(self) -> str:
        """Popis zakončení coby textový řetězec."""
        return self._desc

    @abstractmethod
    def is_end(self, board_snapshot: BoardSnapshot):
        """Abstraktní metoda, která umožňuje rozpoznat zakončení. Typicky,
        jde-li o koncovou kombinaci označených políček, vyhazuje příslušnou
        výjimku, konkrétně `Win` nebo `Draw`.
        """

    @staticmethod
    def find_closure(x: int, y: int, closures: Iterable[FieldClosure]):
        """Pomocná statická metoda pro vyhledávání obálky políčka podle
        dodaných souřadnic políčka.
        """
        for closure in closures:
            if closure.coords == (x, y):
                return closure
        raise Exception(
            f"Obálka políčka se souřadnicemi [{x}, {y}] nebyla nalezena")


class Column(EndRecognizer):
    """Instance této třídy poskytují službu vyhledávání spojení políček ve
    sloupci dle dodaného snímku rozložení hrací plochy.
    """

    def __init__(self, column_number: int):
        """Initor, který přijímá číslo sloupce, který má být prohledáván.
        Z podstaty hry se očekává počítání od nuly.
        """
        EndRecognizer.__init__(
            self, f"Hráč spojil políčka v {column_number + 1}. sloupci.")
        self._column_number = column_number

    @property
    def column_number(self) -> int:
        """Číslo prohledávaného sloupce."""
        return self._column_number

    def is_end(self, board_snapshot: BoardSnapshot):
        """Metoda poskytující službu prohledání snímku rozložení políček hry
        s cílem zjistit, zda-li nebyl spojen některým z hráčů celý sloupec.

        Pokud k takové situaci došlo, znamená to výhru daného hráče a je tedy
        vyhozena výjimka `Win`.
        """
        closures = board_snapshot.field_closures
        characters = []

        # Pro všechny řádky ve sloupečku si zaznamenej znak, kterým se obálka
        # políčka prezentuje
        for y in range(board_snapshot.board_base):
            characters.append(
                self.find_closure(self.column_number, y, closures).character)

        # Pokud je mezi znaky jen jediný společný (unikátní) znak, znamená
        # to, že je sloupec spojen
        if len(set(characters)) == 1:
            raise Win()


class Row(EndRecognizer):
    """Instance této třídy poskytují službu vyhledávání spojení políček v
    řádku dle dodaného snímku rozložení hrací plochy.
    """

    def __init__(self, row_number: int):
        """Initor, který přijímá číslo řádku, který má být prohledáván.
        Z podstaty hry se očekává počítání od nuly.
        """
        EndRecognizer.__init__(
            self, f"Hráč spojil políčka v {row_number + 1}. řádku.")
        self._row_number = row_number

    @property
    def row_number(self) -> int:
        """Prohledávaný řádek"""
        return self._row_number

    def is_end(self, board_snapshot: BoardSnapshot):
        """Metoda poskytující službu prohledání snímku rozložení políček hry
        s cílem zjistit, zda-li nebyl spojen některým z hráčů celý řádek.

        Pokud k takové situaci došlo, znamená to výhru daného hráče a je tedy
        vyhozena výjimka `Win`.
        """
        closures = board_snapshot.field_closures
        characters = []

        for x in range(board_snapshot.board_base):
            characters.append(
                self.find_closure(x, self.row_number, closures).character)

        # Pokud je mezi znaky jen jediný společný (unikátní) znak, znamená
        # to, že je řádek spojen
        if len(set(characters)) == 1:
            raise Win()


class NoMoreMoves(EndRecognizer):
    """Instance této třídy mají za cíl rozpoznávat, že v hracím poli neexistuje
    již žádný další možný tah. Takový stav pak typicky znamená remízu."""

    def __init__(self):
        """Bezparametrický initor, který iniciuje předka."""
        EndRecognizer.__init__(self, "Již není žádný další možný tah.")

    def is_end(self, board_snapshot: BoardSnapshot):
        """Metoda umožňující kontrolu, že hrací plocha již nemá žádných
        dalších možných tahů. Pokud k této situaci skutečně nastane, znamená
        to remízu.
        """
        if len(board_snapshot.valid_moves) == 0:
            raise Draw()


class RightLeftDiagonal(EndRecognizer):
    """Instance této třídy poskytují službu rozpoznání zakončení hry spojením
    diagonálních políček hrací plochy jedním hráčem. Takovýto tah ústí ve
    výhru."""

    def __init__(self):
        """Bezparametrický initor, který iniciuje předka."""
        EndRecognizer.__init__(
            self, "Hráč spojil políčka na pravolevé diagonále")

    def is_end(self, board_snapshot: BoardSnapshot):
        """Metoda, která poskytuje rozhodnutí, zda-li je hra zakončena
        spojením diagonálních políček z levého horního rohu hrací plochy
        k tomu pravému dolnímu.

        Pokud jsou tato políčka spojena, resp. označena jedním hráčem, pak
        je vyhozena výjimka reprezentující výhru.
        """
        closures = board_snapshot.field_closures
        chars = []

        for i in range(board_snapshot.board_base):
            chars.append(self.find_closure(i, i, closures).character)

        if len(set(chars)) == 1:
            raise Win()


class LeftRightDiagonal(EndRecognizer):
    """Instance této třídy poskytují službu rozpoznání zakončení hry spojením
    diagonálních políček hrací plochy jedním hráčem. Takovýto tah ústí ve
    výhru."""

    def __init__(self):
        """Bezparametrický initor, který iniciuje předka."""
        EndRecognizer.__init__(
            self, "Hráč spojil políčka na levopravé diagonále")

    def is_end(self, board_snapshot: BoardSnapshot):
        """Metoda, která poskytuje rozhodnutí, zda-li je hra zakončena
        spojením diagonálních políček z pravého horního rohu hrací plochy
        k tomu levému dolnímu.

        Pokud jsou tato políčka spojena, resp. označena jedním hráčem, pak
        je vyhozena výjimka reprezentující výhru.
        """
        closures = board_snapshot.field_closures
        chars = []

        for i in range(board_snapshot.board_base):
            chars.append(self.find_closure(
                i, (board_snapshot.board_base - 1) - i, closures).character)

        if len(set(chars)) == 1:
            raise Win()


