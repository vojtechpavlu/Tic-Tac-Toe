"""Tento modul obsahuje prostředky pro práci s políčkem.

Konkrétně obsahuje především definici třídy políčka (`Field`), která poskytuje
abstrakci nad samotným políčkem hry.

Dále obsahuje definici konkrétní výjimky, která je vyhozena, dojde-li k
problému na úrovni políčka.
"""


class Field:
    """Instance této třídy reprezentují políčka piškvorek.

    Každé políčko má vlastní souřadnice (reprezentující polohu na hrací ploše)
    a své označení - používané pro reprezentaci tahu hráče.
    """

    # Povolené značky
    __AVAILABLE_MARKS = ("X", "O")

    def __init__(self, x: int, y: int, mark: str = ""):
        """Initor, který přijímá souřadnice políčka na hrací ploše
        specifikovaných jako souřadnice na osách `x` a `y`. Dále přijímá
        označení políčka (`mark`), které může nést pouze omezené hodnoty.

        Konkrétně lze políčko označit prázdným řetězcem, pak jde o neoznačené
        políčko. Alternativně ho lze označit ještě křížkem (znakem `X`) nebo
        kolečkem (znakem `O`) - viz třídní proměnná `__AVAILABLE_MARKS`.
        """
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

    @property
    def copy(self) -> "Field":
        """Vrací kopii tohoto objektu."""
        return Field(self.x, self.y, self.mark)

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


class FieldClosure:
    """Instance této třídy slouží jako obálka políčka, které má být ukryto
    před kýmkoliv co do změny - aby ho nebylo možné libovolně měnit za účelem
    podvádění. Přesto instance této třídy umožňují vystavit důležité aspekty
    políčka."""

    def __init__(self, field: Field):
        """Initor, který přijímá obalované políčko a zástupný znak, kterým má
        být políčko symbolizováno.
        """
        self.__field = field

    @property
    def mark(self) -> str:
        """Značka na políčku. Pokud na tomto políčku ještě nebylo taženo,
        je vrácen prázdný textový řetězec."""
        return self.__field.mark

    @property
    def is_marked(self) -> bool:
        """Vrací, zda-li bylo políčko označeno či nikoliv."""
        return self.__field.is_marked

    @property
    def identifier(self) -> str:
        """Textová reprezentace obálky políčka. Konkrétně jde o znak či soubor
        znaků, které políčko vizuálně symbolizují.

        Bylo-li již na políčku taženo, pak vrátí značku obalovaného políčka.
        V opačném případě vrací souřadnice políčka ve formátu `X Y`."""
        return self.mark or f"{self.__field.x} {self.__field.y}"

    @property
    def coords(self) -> tuple[int, int]:
        """Souřadnice políčka, které je touto instancí obaleno."""
        return self.__field.xy


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



