
import pytest

from src.game.game import Game, GameError
from test.dummy_player import DummyPlayer


@pytest.fixture
def players():
    return [DummyPlayer("dummy1", "X"), DummyPlayer("dummy2", "O")]


def test_game_creation_success(players):
    assert Game(players)


def test_game_creation_no_players():
    with pytest.raises(GameError) as ge:
        assert Game([])


def test_game_creation_only_one_player():
    with pytest.raises(GameError) as ge:
        assert Game([DummyPlayer("SinglePlayer", "X")])




