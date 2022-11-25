import pytest

from src.game.field import Field, FieldClosure, FieldError


@pytest.fixture
def field():
    return Field(1, 1)


def test_closure_coords(field):
    field.mark = "X"
    assert FieldClosure(field).coords == (1, 1)


def test_closure_if_can_be_created_with_mark(field):
    assert not field.is_marked
    field.mark = "X"
    FieldClosure(field)


def test_closure_if_can_be_created_without_mark(field):
    assert not field.is_marked
    FieldClosure(field)


def test_closure_if_holds_the_info_about_its_mark(field):
    assert not field.is_marked
    assert not FieldClosure(field).is_marked
    field.mark = "X"
    assert FieldClosure(field).is_marked


def test_closure_if_returns_coords_of_unmarked_field(field):
    assert not field.is_marked
    assert FieldClosure(field).identifier == "1 1"


def test_closure_if_does_not_returns_coords_of_marked_field(field):
    assert not field.is_marked
    field.mark = "X"
    assert FieldClosure(field).identifier == "X"

