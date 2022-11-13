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


def test_game_creation_more_than_two_players():
    with pytest.raises(GameError) as ge:
        assert Game([
            DummyPlayer("Triplet1", "X"),
            DummyPlayer("Triplet2", "X"),
            DummyPlayer("Triplet3", "X")
        ])


def test_game_creation_two_players_with_same_mark():
    with pytest.raises(GameError) as ge:
        assert Game([DummyPlayer("A", "X"), DummyPlayer("B", "X")])


def test_game_returns_players():
    game = Game([DummyPlayer("A", "X"), DummyPlayer("B", "O")])
    assert len(game.players) == 2
    assert game.players[0].player_name == "A"
    assert game.players[1].player_name == "B"


def test_game_returns_player_names():
    game = Game([DummyPlayer("A", "X"), DummyPlayer("B", "O")])
    assert game.player_names == ("A", "B")
