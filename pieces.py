

class Piece(object):
    def __init__(self, _row: int, _column: int, _colour: str):
        self.colour = _colour
        self.row = _row
        self.column = _column
        self.multi_moves = False
        self.icon_asset = None
        if self.colour == "white":
            self.colour_code = (255, 255, 255, 0)
        else:
            self.colour_code = (0, 0, 0, 0)


class Pawn(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        if self.row < 2:
            self.moves = [[1, 0], [1, 1], [1, -1]]
        else:
            self.moves = [[-1, 0], [-1, 1], [-1, -1]]

    def __repr__(self):
        if self.colour == "white":
            return 'P'
        else:
            return 'p'


class Knight(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        self.moves = [[2, 1], [1, 2], [-2, 1], [-2, -1], [2, -1], [-1, 2], [-1, -2], [1, -2]]

    def __repr__(self):
        if self.colour == "white":
            return 'N'
        else:
            return 'n'


class Bishop(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        self.moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        self.multi_moves = True

    def __repr__(self):
        if self.colour == "white":
            return 'B'
        else:
            return 'b'


class Rook(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        self.moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.multi_moves = True
        self.has_moved = False

    def __repr__(self):
        if self.colour == "white":
            return 'R'
        else:
            return 'r'


class Queen(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        self.moves = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        self.multi_moves = True

    def __repr__(self):
        if self.colour == "white":
            return 'Q'
        else:
            return 'q'


class King(Piece):
    def __init__(self, _row, _column, _colour):
        super().__init__(_row, _column, _colour)
        self.moves = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        self.has_moved = False
        self.in_check = False
        self.has_castled = False

    def __repr__(self):
        if self.colour == "white":
            return 'K'
        else:
            return 'k'
