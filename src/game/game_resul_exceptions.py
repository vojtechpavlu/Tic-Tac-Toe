""""""


class Win(Exception):
    """"""


class Draw(Exception):
    """"""


class GameOver(Exception):
    """"""

    def __init__(self, message: str):
        """"""
        Exception.__init__(self, message)



