
import pytest

from src.game.board import BoardSnapshot, default_board


@pytest.fixture
def fields():
    return default_board().fields


@pytest.fixture
def board():
    return default_board()


def test_create_board_snapshot(board):
    assert BoardSnapshot(board)


def test_empty_fields_without_move(board, fields):
    assert len(BoardSnapshot(board).empty_fields) == len(fields)


def test_empty_fields_with_one_move(board, fields):
    board.mark(1, 1, "X")
    assert len(BoardSnapshot(board).empty_fields) == len(fields) - 1


def test_played_fields_without_move(board):
    assert len(BoardSnapshot(board).played_fields) == 0


def test_played_fields_with_one_move(board):
    board.mark(1, 1, "X")
    assert len(BoardSnapshot(board).played_fields) == 1


def test_valid_moves_without_move(board, fields):
    assert len(BoardSnapshot(board).valid_moves) == len(fields)


def test_valid_moves_after_one_move(board, fields):
    board.mark(1, 1, "X")
    assert len(BoardSnapshot(board).valid_moves) == len(fields) - 1



