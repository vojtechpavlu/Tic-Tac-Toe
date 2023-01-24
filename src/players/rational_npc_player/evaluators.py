""""""

from abc import ABC, abstractmethod


class Evaluator(ABC):
    """Abstraktní třída, jejíž potomci jsou odpovědni za implementaci
    abstraktní metody `evaluate`, která poskytuje službu získání hodnoty
    užitku pro danou hrací plochu daného sledovaného hráče.
    """

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






