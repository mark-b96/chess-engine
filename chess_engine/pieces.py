from typing import Tuple


class Piece:
    def __init__(self, row, column, colour, symbol):
        self.row: int = row
        self.column: int = column
        self.colour: str = colour
        self.symbol: str = symbol
        self.multi_moves = False
        self.icon_asset = None
        self.has_moved = False
        self.moves = None

        if self.colour == "white":
            self.colour_code = (255, 255, 255, 0)
        else:
            self.colour_code = (0, 0, 0, 0)

    def get_moves(self) -> Tuple:
        return self.moves

    def __repr__(self):
        if self.colour == "white":
            return self.symbol.upper()
        else:
            return self.symbol

    def __str__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        if self.colour == "black":
            self.moves = ((1, 0), (1, 1), (1, -1))
            if row != 1:
                self.has_moved = True
        else:
            self.moves = ((-1, 0), (-1, 1), (-1, -1))
            if row != 6:
                self.has_moved = True

        self.value = 1

    def is_being_promoted(self, dst_row: int) -> bool:
        if self.colour == "white" and dst_row == 0:
            return True
        if self.colour == "black" and dst_row == 7:
            return True


class Knight(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        self.moves = (
            (2, 1),
            (1, 2),
            (-2, 1),
            (-2, -1),
            (2, -1),
            (-1, 2),
            (-1, -2),
            (1, -2),
        )
        self.value = 3


class Bishop(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        self.moves = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        self.multi_moves = True
        self.value = 3


class Rook(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        self.moves = ((1, 0), (0, 1), (-1, 0), (0, -1))
        self.multi_moves = True
        self.value = 5
        self.starting_position = (row, column)


class Queen(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        self.moves = (
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        )
        self.multi_moves = True
        self.value = 9


class King(Piece):
    def __init__(self, row, column, colour, symbol):
        super().__init__(row, column, colour, symbol)
        self.moves = (
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        )
        self.in_check = False
        self.has_castled = False
        self.value = 0
        self.castling_status = []
