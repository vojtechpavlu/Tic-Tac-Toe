import pytest

from src.game.field import Field, FieldClosure, FieldError


@pytest.fixture
def field():
    return Field(1, 1)


def test_create_field_closure(field):
    assert FieldClosure(field, "2")


def test_create_field_closure_with_substitute(field):
    assert FieldClosure(field, "2")


def test_has_substitute_positive(field):
    assert FieldClosure(field, "2").has_substitute_character


def test_has_substitute_negative(field):
    field.mark = "X"
    assert not FieldClosure(field).has_substitute_character


def test_closure_coords(field):
    field.mark = "X"
    assert FieldClosure(field).coords == (1, 1)


def test_closure_check_with_mark(field):
    assert not field.is_marked
    field.mark = "X"
    FieldClosure(field)


def test_closure_check_without_mark(field):
    assert not field.is_marked
    FieldClosure(field, "2")


def test_closure_check_without_both(field):
    assert not field.is_marked

    with pytest.raises(FieldError) as fe:
        FieldClosure(field)  # Nemá značku ani zástupný symbol


def test_closure_check_with_both(field):
    assert not field.is_marked

    field.mark = "X"

    with pytest.raises(FieldError) as fe:
        FieldClosure(field, "2")  # Má značku a zástupný symbol



