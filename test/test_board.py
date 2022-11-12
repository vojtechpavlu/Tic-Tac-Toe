import pytest

from src.game.board import Board
from src.game.field import Field


def fields():
    all_fields = []
    for y in range(3):
        for x in range(3):
            all_fields.append(Field(x, y))
    return all_fields


@pytest.fixture
def board():
    return Board(fields())


def test_board_creation(board):
    assert board


def test_finding_field_positive(board):
    assert board.has_field(1, 1)   # Určitě má


def test_finding_field_negative(board):
    assert not board.has_field(-1, -1)   # Určitě nemá


def test_field_search_positive(board):
    assert board.field(1, 1) is not None


def test_field_search_negative(board):
    assert board.field(-1, -1) is None


def test_number_of_fields(board):
    assert board.size == 9


def test_fields_with_and_without_mark(board):
    assert len(board.marked_fields) == 0
    assert len(board.unmarked_fields) == 9

    # Označení jednoho políčka
    board.field(1, 1).mark = "X"

    assert len(board.marked_fields) == 1
    assert len(board.unmarked_fields) == 8







