""""""

from typing import Iterable

from src.game.board import Board, default_board, BoardSnapshot
from src.game.player import Player


class Game:
    """Reprezentace hry dvou hráčů."""

    def __init__(self, players: Iterable[Player],
                 board: Board = default_board()):
        """Initor, který přijímá sadu hráčů a hrací plochu, na které má hra
        probíhat.

        Hra předpokládá několik vlastností, které hráči musí splnit. V první
        řadě musí být právě 2 hráči, dále pak musí mít každý přidělen unikátní
        znak, kterým označují políčka svých tahů. Nejsou-li tyto podmínky
        splěny, je vyhozena výjimka.
        """
        self.__players = list(players)
        self.__board = board

        # Kontrola, že jsou dodaní hráči validní. Pokud by nebyli,
        # byla by vyhozena výjimka
        self.__check_players()

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

    def run_game(self):
        index = 0

        # Nekonečný cyklus
        while True:

            # Hra dvou hráčů - střídají se (podobně jako sudá a lichá čísla)
            player = self.players[index % 2]
            print("Na tahu je hráč:", player.player_name)

            snapshot = self.__board.board_snapshot

            # Vyzvání hráče ke svému tahu, získání odpovědi a očištění
            # této odpovědi
            player_move = player.move(snapshot, snapshot.valid_moves)
            player_move = self.__clear_player_input(player_move)

            # Zkontroluj, že uživatel zadal validní vstup. Pokud nezadal,
            # opakuj tuto iteraci znovu
            if not self.__check_player_input(snapshot, player_move):
                continue

            # Pokud uživatel zadal validní tah, proveď ho - označ políčko,
            # které specifikoval uživatel
            for closure in snapshot.field_closures:
                if player_move == closure.character:
                    self.__board.mark(*closure.coords, player.mark)
                    break

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

    @staticmethod
    def __clear_player_input(player_input: str) -> str:
        """"""
        return player_input.strip().lower()

    @staticmethod
    def __check_player_input(board_snapshot: BoardSnapshot,
                             player_input: str) -> bool:
        """"""
        if player_input not in board_snapshot:
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


