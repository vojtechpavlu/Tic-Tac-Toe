""""""


class Field:
    """"""

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
        self.__mark = new_mark

    @property
    def is_marked(self) -> bool:
        """Vrací, zda-li je políčko označeno či nikoliv."""
        return self.mark != ""

    @staticmethod
    def check_mark(mark: str):
        """Kontroluje, zda-li je dodaná značka korektní. Pokud není, je
        vyhozena výjimka."""
        if len(mark) > 1:
            raise ValueError(f"Očekávaná délka je 0 nebo jeden znak: "
                             f"'{mark}'")





