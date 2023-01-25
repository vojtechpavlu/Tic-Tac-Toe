"""Balíček hráčů obsahuje definice jednotlivých tříd hráčů. Ti mají společného
abstraktního předka `Player`, který slouží jako deklarace obecného,
neinstaciovatelného protokolu pro všechny hráče.

Tento modul má za cíl fungovat jako zkratka pro snazší a přehlednější import
všech hráčů.
"""

from .human_player.human_player import HumanPlayer
from .random_player.random_npc_player import RandomNPCPlayer
from .custom_player.custom_player import CustomPlayer
from .rational_npc_player import MinmaxNPC, LimitedMinmaxPlayer
