import pytest

from src.game.player import PlayerError
from test.dummy_player import DummyPlayer


def test_player_creation_success():
    assert DummyPlayer("test_player", "X")
    assert DummyPlayer("test_player", "O")


def test_player_creation_wrong_name():
    with pytest.raises(PlayerError) as pe:
        DummyPlayer("", "X")


def test_player_creation_empty_mark():
    with pytest.raises(PlayerError) as pe:
        DummyPlayer("test_player", "")


def test_player_creation_wrong_mark():
    with pytest.raises(PlayerError) as pe:
        DummyPlayer("test_player", "WRONG_MARK")


def test_player_name_population():
    player = DummyPlayer("test_player", "X")
    assert player.player_name == "test_player"


def test_player_mark_population():
    player = DummyPlayer("test_player", "X")
    assert player.mark == "X"

