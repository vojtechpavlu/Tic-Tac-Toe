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




