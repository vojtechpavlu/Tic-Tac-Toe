""""""


class Field:
    """"""

    __AVAILABLE_MARKS = ("X", "O")

    def __init__(self, x: int, y: int, mark: str = ""):
        self.__x = x
        self.__y = y
        self.__mark = mark

        self.check_mark(mark)

    @property
    def x(self) -> int:
        """Souřadnice tohoto políčka na ose x."""
        return self.__x

    @x.setter
    def x(self, new_x: int):
        """Nastaví souřadnici na ose x tohoto políčka"""
        self.__x = new_x

    @property
    def y(self) -> int:
        """Souřadnice tohoto políčka na ose y."""
        return self.__y

    @y.setter
    def y(self, new_y: int):
        """Nastaví souřadnici na ose y tohoto políčka"""
        self.__y = new_y

    @property
    def xy(self) -> tuple[int, int]:
        """Ntice reprezentující obě souřadnice tohoto políčka."""
        return self.x, self.y

    @property
    def mark(self) -> str:
        """Znak, kterým je dané políčko označeno."""
        return self.__mark

    @mark.setter
    def mark(self, new_mark: str):
        """Nastavuje znak, kterým je dané políčko označeno."""
        self.check_mark(new_mark)
        if self.is_marked:
            raise FieldError(f"Značku nelze znovu změnit!", self)
        self.__mark = new_mark

    @property
    def is_marked(self) -> bool:
        """Vrací, zda-li je políčko označeno či nikoliv."""
        return self.mark != ""

    @classmethod
    def available_marks(cls) -> tuple[str, str]:
        """Značky, kterými je možné políčko označit."""
        return cls.__AVAILABLE_MARKS

    @staticmethod
    def check_mark(mark: str):
        """Kontroluje, zda-li je dodaná značka korektní. Pokud není, je
        vyhozena výjimka."""
        if len(mark) > 1:
            raise FieldError(f"Očekávaná délka je 0 nebo jeden znak: "
                             f"'{mark}'")
        elif len(mark) == 1 and mark not in Field.available_marks():
            raise FieldError(
                f"Neočekávaná značka: '{mark}'. "
                f"Zkus některou z: {Field.available_marks}")


class FieldError(Exception):
    """Instance této třídy reprezentují chybu, která může nastat v momentě
    práce s políčkem.

    Kromě standardní výjimky je vybavena i referencí na políčko, v jehož
    kontextu k chybě došlo."""

    def __init__(self, message: str, field: Field = None):
        """Initor, který přijímá textovou zprávu o chybě a referenci na
        políčko, v jehož kontextu k chybě došlo. Tento parametr je defaultně
        nastaven jako None (jde o nepovinnou složku).
        """
        Exception.__init__(self, message)
        self._field = field

    @property
    def has_field(self) -> bool:
        """Vrací, zda-li bylo výjimce poskytnuto políčko."""
        return self.field is not None

    @property
    def field(self) -> Field:
        """Políčko, v jehož kontextu došlo k chybě."""
        return self._field



