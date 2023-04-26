

SQUARE_COLOUR_CODES = {
    "white": (0, 128, 128),
    "black": (21, 71, 52),
}


class Square:
    def __init__(self, row: int, column: int, colour: str):
        self.row: int = row
        self.column: int = column
        self.colour: str = colour
        self.columns_str: str = "abcdefgh"
        self.colour_code = SQUARE_COLOUR_CODES[self.colour]
        self.piece, self.promotion_piece = None, None

    def __repr__(self):
        if self.piece:
            return self.piece.__repr__()
        else:
            return "0" if self.colour == "white" else "1"

    def __str__(self):
        row = 8 - self.row
        column = self.columns_str[self.column]
        return f"{column}{row}"
