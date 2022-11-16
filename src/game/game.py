"""Tento modul obsahuje všechny prostředky pro management životního cyklu hry.

Především pak obsahuje definici třídy, která hru reprezentuje (`Game`)."""

from typing import Iterable

from src.game.board import Board, default_board, BoardSnapshot
from src.game.end_recognition import (EndRecognizer, Column, NoMoreMoves, Row,
                                      LeftRightDiagonal, RightLeftDiagonal)
from src.game.game_resul_exceptions import Draw, GameOver, Win
from src.game.player import Player


class Game:
    """Reprezentace hry dvou hráčů."""

    def __init__(self, players: Iterable[Player],
                 board: Board = None):
        """Initor, který přijímá sadu hráčů a hrací plochu, na které má hra
        probíhat.

        Hra předpokládá několik vlastností, které hráči musí splnit. V první
        řadě musí být právě 2 hráči, dále pak musí mít každý přidělen unikátní
        znak, kterým označují políčka svých tahů. Nejsou-li tyto podmínky
        splěny, je vyhozena výjimka.
        """
        self.__players = list(players)
        self.__board = board or default_board()
        self.__end_recognizers: list[EndRecognizer] = []

        # Kontrola, že jsou dodaní hráči validní. Pokud by nebyli,
        # byla by vyhozena výjimka
        self.__check_players()

        self.__set_up_end_recognizers()

    @property
    def players(self) -> tuple[Player]:
        """Vrací ntici všech hráčů, kteří ve hře jsou."""
        return tuple(self.__players)

    @property
    def player_names(self) -> tuple[str]:
        """Vrací ntici jmen všech hrářů."""
        return tuple([player.player_name for player in self.players])

    @property
    def player_marks(self) -> tuple[str]:
        """Vrací ntici všech značek, které hráči používají k označování políček
        svých tahů."""
        return tuple([player.mark for player in self.players])

    @property
    def end_recognizers(self) -> tuple[EndRecognizer]:
        """"""
        return tuple(self.__end_recognizers)

    def run_game(self):
        """Jednoduchá implementace, která umožňuje teoreticky do nekonečna
        střídat tahy hráčů, případně je zopakovat v případě chyby.
        """
        index = 0

        # Nekonečný cyklus
        while True:

            # Hra dvou hráčů - střídají se (podobně jako sudá a lichá čísla)
            player = self.players[index % 2]
            print(80*"-")
            print("Na tahu je hráč:", player.player_name)

            snapshot = self.__board.board_snapshot

            # Vyzvání hráče ke svému tahu, získání odpovědi a očištění
            # této odpovědi
            player_move = player.move(snapshot, snapshot.valid_moves)
            player_move = self.__clear_player_input(player_move)

            # Zkontroluj, že uživatel zadal validní vstup. Pokud nezadal,
            # opakuj tuto iteraci znovu
            if not self.__check_player_input(snapshot, player_move):
                print(f"Neplatný tah: '{player_move}'")
                continue

            # Pokud uživatel zadal validní tah, proveď ho - označ políčko,
            # které specifikoval uživatel
            for closure in snapshot.field_closures:
                if player_move == closure.character:
                    self.__board.mark(*closure.coords, player.mark)
                    break

            # Pro každý rozpoznávač zkontroluj
            for end_recognizer in self.end_recognizers:
                try:
                    end_recognizer.is_end(self.__board.board_snapshot)

                # Pokud je daný stav remízou
                except Draw:
                    raise GameOver(
                        f"Hra skončila remízou - {end_recognizer.description}")

                # Pokud je daný stav výhrou jednoho z hráčů
                except Win:
                    raise GameOver(f"Hráč '{player.player_name}' vyhrál - "
                                   f"{end_recognizer.description}")

            # Další tah
            index += 1

    def __check_players(self):
        """Kontrola validity hráčů. Kontroluje se následující:

            - Počet hráčů - musí být právě dva hráči
            - Značky, kterými hráči označují svá políčka - musí být unikátní
        """
        # Pokud je počet hráčů jiný než 2
        if len(self.players) != 2:
            raise GameError(f"Počet hráčů musí být 2: "
                            f"{len(self.players)}", self)

        # Pokud je počet unikátních značek jiný, než počet hráčů
        elif len(set(self.player_marks)) != len(self.players):
            raise GameError(
                f"Každý hráč musí mít unikátní značku: "
                f"{self.player_marks}", self)

    def __set_up_end_recognizers(self):
        """Privátní metoda, která se stará o opatření služebníků, kteří
        mají za cíl rozpoznávat konečné (výherní či remízové) rozložení
        hrací plochy.
        """
        # Rozpoznávače spojení sloupců a řádků
        for i in range(3):
            self.__end_recognizers.append(Column(i))
            self.__end_recognizers.append(Row(i))

        # Rozpoznávače spojení diagonál
        self.__end_recognizers.append(LeftRightDiagonal())
        self.__end_recognizers.append(RightLeftDiagonal())

        # Rozpoznávač, když neexistuje další tah (remíza)
        self.__end_recognizers.append(NoMoreMoves())

    @staticmethod
    def __clear_player_input(player_input: str) -> str:
        """Očišťuje hráčův vstup o mezery a převádí ho na malá písmena."""
        return player_input.strip().lower()

    @staticmethod
    def __check_player_input(board_snapshot: BoardSnapshot,
                             player_input: str) -> bool:
        """Formální kontrola vstupu, zda-li je možné takový tah provést."""
        if player_input not in board_snapshot.valid_moves:
            return False
        return True


class GameError(Exception):
    """Výjimka reprezentující problém, ke kterému došlo během práce s instancí
    třídy `Game`. Svého předka rozšiřuje o schopnost udržení reference na hru,
    v jejímž kontextu došlo k chybě."""

    def __init__(self, message: str, game: Game):
        """Initor, který přijímá textovou zprávu o chybě a referenci na objekt
        hry, v jejímž kontextu došlo k chybě."""
        Exception.__init__(self, message)
        self._game = game

    @property
    def game(self) -> Game:
        """Instance hry (třídy `Game`), v jejímž kontextu došlo k chybě."""
        return self._game


