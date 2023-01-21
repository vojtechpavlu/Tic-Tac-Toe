"""Tento modul obsahuje funkční definici zakončení hry.

Rozlišuje přitom obecné zakončení, výhru a remízu. Tato jsou reprezentována
pomocí výjimek - `Win`, `Draw` a `GameOver`."""


class Win(Exception):
    """Výjimka reprezentující výhru hráče.

    Typickým výherním zakončením je spojení políček ve sloupci, v řádku
    nebo na diagonále."""


class Draw(Exception):
    """Výjimka reprezentující remízu mezi hráči.

    Případem, kdy může dojít k remíze je, kdy již neexistují žádné další možné
    tahy a přesto nejde o výherní rozložení ani pro jednoho z hráčů.
    """


class GameOver(Exception):
    """Obecné zakončení hry.

    Tato reprezentace výjimkou umožňuje její probublání do volajících instancí
    a tím umožňuje probublat až k instanci první kategorie.
    """

    def __init__(self, winner: str, message: str):
        """Initor, který přijímá jméno hráče, který vyhrál a textovou
        reprezentaci zprávy o ukončení hry.
        """
        Exception.__init__(self, message)
        self.__winner = winner

    @property
    def winner(self) -> str:
        """Jméno hráče, který vyhrál. Pokud hra skončila remízou, vrací None.
        """
        return self.__winner



