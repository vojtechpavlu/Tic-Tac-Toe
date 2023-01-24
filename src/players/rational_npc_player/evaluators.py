""""""

from abc import ABC, abstractmethod


class Evaluator(ABC):
    """Abstraktní třída, jejíž potomci jsou odpovědni za implementaci
    abstraktní metody `evaluate`, která poskytuje službu získání hodnoty
    užitku pro danou hrací plochu daného sledovaného hráče.
    """

    def __init__(self, ratio: float = 1):
        """"""
        self.__ratio = ratio

    @property
    def ratio(self) -> float:
        """"""
        return self.__ratio

    @abstractmethod
    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Abstraktní metoda, která definuje společnou signaturu k povinnému
        překrytí. Význam této metody je k vyhodnocení aktuálního rozložení
        co do výplatní funkce pro sledovaného hráče.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající užitku plynoucího z daného rozložení
            pro sledovaného hráče
        """


class WinInRow(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění výhry v řádku hrací
    plochy.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do výhry
        v řádku, tedy spojení všech políček v některém z řádků hrací plochy.
        V takovém případě vrací výherní hodnotu (konkrétně `1000.0`).

        Algoritmus prochází každý řádek zvlášť a z každého si vybere unikátní
        hodnoty. Pokud je jen jediná unikátní hodnota v daném řádku a odpovídá
        značce sledovaného hráče, funkce vrací výherní hodnotu.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do spojení řádku

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající výhře hráče
        """
        for line in board:
            uniques = tuple(set(line))
            if len(uniques) == 1 and uniques[0] == player_mark:
                return 1000.0
        return 0


class WinInColumn(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění výhry ve sloupci hrací
    plochy.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do výhry
        ve sloupci, tedy spojení všech políček v některém ze sloupců hrací
        plochy. V takovém případě vrací výherní hodnotu (konkrétně `1000.0`).

        Algoritmus prochází každý sloupec zvlášť a z každého si vybere
        unikátní hodnoty. Pokud je jen jediná unikátní hodnota v daném
        sloupci a tato odpovídá značce sledovaného hráče, funkce vrací
        výherní hodnotu.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do spojení sloupce

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající výhře hráče
        """
        size = len(board)
        for x in range(size):
            column = [board[y][x] for y in range(size)]
            uniques = tuple(set(column))
            if len(uniques) == 1 and uniques[0] == player_mark:
                return 1000.0
        return 0


class WinInFirstDiagonal(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění výhry v první diagonále,
    tedy té vedoucí z levého horního rohu do pravého dolního.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do výhry
        v diagonále. V takovém případě vrací výherní hodnotu
        (konkrétně `1000.0`).

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do spojení
            políček na první diagonále

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající výhře hráče
        """
        size = len(board)
        diag = [board[i][i] for i in range(size)]
        uniques = tuple(set(diag))
        if len(uniques) == 1 and uniques[0] == player_mark:
            return 1000.0
        return 0


class WinInSecondDiagonal(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění výhry ve druhé diagonále,
    tedy té vedoucí z levého dolního rohu do pravého horního.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do výhry
        v diagonále. V takovém případě vrací výherní hodnotu
        (konkrétně `1000.0`).

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do spojení
            políček na druhé diagonále

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající výhře hráče
        """
        size = len(board)
        diag = [board[size - 1 - i][i] for i in range(size)]
        uniques = tuple(set(diag))
        if len(uniques) == 1 and uniques[0] == player_mark:
            return 1000.0
        return 0


class OffensiveProgressInRow(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění pozitivního postupu ve
    hře. Konkrétně se tyto instance zaměřují na měření užitku z postupného
    plnění řádků.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do
        postupného plnění řádku. S rostoucím počtem vyplněných políček v
        řádku roste i užitek z tohoto řádku. Pokud je řádek vyplněn byť
        jen jedinou značkou oponenta, již nemá smysl tento řádek uvažovat
        jako jakkoliv užitečný.

        Tento proces je pak proveden nad všemi řádky hrací plochy.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do počtu políček
            daného hráče v jednotlivých řádcích

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající užitku sledovaného hráče
        """
        total = 0
        for row in board:
            if opponent_mark not in row:
                total += row.count(player_mark) ** 2 / len(row)
        return total * self.ratio


class OffensiveProgressInColumn(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění pozitivního postupu ve
    hře. Konkrétně se tyto instance zaměřují na měření užitku z postupného
    plnění sloupců.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do
        postupného plnění sloupce. S rostoucím počtem vyplněných políček
        ve sloupci roste i užitek z tohoto sloupce. Pokud je sloupeček
        vyplněn byť jen jedinou značkou oponenta, již nemá smysl tento
        sloupec uvažovat jako jakkoliv užitečný.

        Tento proces je pak proveden nad všemi sloupci hrací plochy.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do počtu políček
            daného hráče v jednotlivých sloupcích

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající užitku sledovaného hráče
        """
        total = 0
        for x in range(len(board)):
            column = [board[y][x] for y in range(len(board))]
            if opponent_mark not in column:
                total += column.count(player_mark) ** 2 / len(column)
        return total * self.ratio


class OffensiveProgressInFirstDiagonal(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění pozitivního postupu ve
    hře. Konkrétně se tyto instance zaměřují na měření užitku z postupného
    plnění první diagonály, tedy té z vedoucí z levého horního rohu do toho
    pravého spodního.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do
        postupného plnění první diagonály. S rostoucím počtem vyplněných
        políček na diagonále roste i užitek. Pokud je diagonála vyplněna
        byť jen jedinou značkou oponenta, již nemá smysl tuto diagonálu
        uvažovat jako jakkoliv užitečnou.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do počtu políček
            daného hráče na první diagonále (vedoucí z levého horního rohu
            do toho pravého dolního)

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající užitku sledovaného hráče
        """
        length = len(board)
        diagonal = [board[i][i] for i in range(length)]
        if opponent_mark not in diagonal:
            return (diagonal.count(player_mark) ** 2 / length) * self.ratio
        return 0


class OffensiveProgressInSecondDiagonal(Evaluator):
    """Instance této třídy jsou odpovědné za zjištění pozitivního postupu ve
    hře. Konkrétně se tyto instance zaměřují na měření užitku z postupného
    plnění druhé diagonály, tedy té z vedoucí z levého spodního rohu do toho
    pravého horního.
    """

    def evaluate(self, board: list[list[str]], player_mark: str,
                 opponent_mark: str) -> float:
        """Metoda, která má za cíl vyhodnotit otisk hrací plochy co do
        postupného plnění druhé diagonály. S rostoucím počtem vyplněných
        políček na diagonále roste i užitek. Pokud je diagonála vyplněna
        byť jen jedinou značkou oponenta, již nemá smysl tuto diagonálu
        uvažovat jako jakkoliv užitečnou.

        Parameters
        ----------
        board: list[list[str]]
            Otisk hrací plochy, která má být vyhodnocena co do počtu políček
            daného hráče na druhé diagonále (vedoucí z levého dolního rohu
            do toho pravého horního)

        player_mark: str
            Značka, kterou používá sledovaný hráč

        opponent_mark: str
            Značka, kterou používá oponent sledovaného hráče

        Returns
        -------
        float
            Reálné číslo odpovídající užitku sledovaného hráče
        """
        length = len(board)
        diagonal = [board[length - i - 1][i] for i in range(length)]
        if opponent_mark not in diagonal:
            return (diagonal.count(player_mark) ** 2 / length) * self.ratio
        return 0



