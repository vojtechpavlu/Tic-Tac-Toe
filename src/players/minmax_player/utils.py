""""""


from src.game.board import BoardSnapshot


def is_terminate(board: list[list[str]]) -> str:
    """Funkce odpovědná za ověření, zda-li není stav (hrací plocha) již listem
    stromu (terminální uzel). Pokud ano, vrací značku výherce nebo textový
    řetězec `draw`. V opačném případě vrací prázdný řetězec.
    """
    return (check_horizontals(board) or check_verticals(board) or
            check_diagonals(board) or check_draw(board) or "")


def check_horizontals(board: list[list[str]]) -> str:
    """Funkce odpovědná za kontrolu řádků. Pokud jsou v některém z řádků
    vyplněna všechna políčka jedním hráčem, vrací funkce značku tohoto
    hráče, jinak vrací prázdný řetězec.
    """
    for line in board:
        if len(set(line)) == 1:
            return line[0]
    return ""


def check_verticals(board: list[list[str]]) -> str:
    """Funkce odpovědná za kontrolu, zda-li není zcela vyplněn některý ze
    sloupečků hrací plochy značkami jednoho hráče. Pokud ano, vrací jeho
    značku, jinak prázdný řetězec.
    """
    for x in range(len(board[0])):
        line = []
        for y in range(len(board)):
            line.append(board[y][x])
        if len(set(line)) == 1:
            return line[0]
    return ""


def check_diagonals(board: list[list[str]]) -> str:
    """Funkce odpovědná za provedení kontroly obou diagonál. Pokud je alespoň
    jedna diagonála vyplněna stejnou značkou, vrací tuto značku. Jinak vrací
    prázdný řetězec.
    """
    first_diagonal = []
    second_diagonal = []
    for i in range(len(board)):
        first_diagonal.append(board[i][i])
        second_diagonal.append(board[len(board) - i - 1][i])
    if len(set(first_diagonal)) == 1:
        return first_diagonal[0]
    elif len(set(second_diagonal)) == 1:
        return second_diagonal[0]
    else:
        return ""


def check_draw(board: list[list[str]]) -> str:
    """Funkce odpovědná za kontrolu, že hra dospěla, resp. nedospěla do
    remízového stavu. Pokud najde volné políčko, které lze vyplnit, funkce
    vrací prázdný řetězec; pokud takové políčko neexistuje, vrací textový
    řetězec `draw`.
    """
    for y in range(len(board)):
        for x in range(len(board)):
            if not board[y][x]:
                return ""
    return "draw"


def translate_board(board: BoardSnapshot) -> list[list[str]]:
    """Statická metoda odpovědná za převedení hrací plochy v podobě
    instance třídy `BoardSnapshot` do dvoudimenzionálního seznamu
    textových řetězců.
    """
    new_board = []
    base = board.board_base
    for y in range(base):
        new_board.append(
            [board.find_closure(x, y).mark for x in range(base)]
        )
    return new_board
