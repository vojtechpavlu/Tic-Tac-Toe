import pytest
from src.game.field import Field, FieldError

# Definice souřadnic políček
X = 1
Y = 2


@pytest.fixture
def field():
    return Field(X, Y)


def test_field_creation(field):
    assert field

    field = Field(1, 1, "X")
    assert field.mark == "X"

    field = Field(1, 1)
    assert field.mark == ""


def test_field_correct_coords(field):
    assert field.x == X, "Políčko vrací špatné x"
    assert field.y == Y, "Políčko vrací špatné y"


def test_field_encapsulation_single_underscore(field):
    with pytest.raises(Exception) as e:
        a = field._x

    with pytest.raises(Exception) as e:
        a = field._y


def test_field_encapsulation_double_underscore(field):
    with pytest.raises(Exception) as e:
        a = field.__x

    with pytest.raises(Exception) as e:
        a = field.__y


def test_coords_change(field):
    field.x = 4
    field.y = 5

    assert field.xy == (4, 5)


def test_is_marked_negative(field):
    assert not field.is_marked


def test_is_marked_positive(field):
    field.mark = "X"
    assert field.is_marked


def test_field_available_marks():
    assert Field.available_marks() == ("X", "O")


def test_wrong_mark(field):
    assert not field.is_marked

    with pytest.raises(FieldError) as fe:
        field.mark = "W"


def test_multiple_characters():
    with pytest.raises(FieldError) as fe:
        field = Field(1, 1, "WRONG")


def test_overwrite(field):
    assert not field.is_marked

    field.mark = "X"  # Nastav validní značku

    assert field.is_marked

    with pytest.raises(FieldError) as fe:
        field.mark = "O"


def test_mark_empty(field):
    assert not field.is_marked

    field.mark = "X"  # Nastav validní značku

    assert field.is_marked

    with pytest.raises(FieldError) as fe:
        field.mark = ""





