import pytest

from src.game.field import Field, FieldClosure


@pytest.fixture
def field():
    return Field(1, 1)


def test_create_field_closure(field):
    assert FieldClosure(field)


def test_create_field_closure_with_substitute(field):
    assert FieldClosure(field, "2")


def test_has_substitute_positive(field):
    assert FieldClosure(field, "2").has_substitute_character


def test_has_substitute_negative(field):
    assert not FieldClosure(field).has_substitute_character


def test_closure_coords(field):
    assert FieldClosure(field).coords == (1, 1)


