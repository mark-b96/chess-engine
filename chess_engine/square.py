
class Square:
    def __init__(self, row, column, colour):
        self.row: int = row
        self.column: int = column
        self.colour: str = colour
        self.piece = None
        self.columns_str: str = 'abcdefgh'
        self.promotion_piece = None
        if self.colour == 'white':
            self.colour_code = (0, 128, 128)
        else:
            self.colour_code = (21, 71, 52)

    def __repr__(self):
        if self.piece:
            return self.piece.__repr__()
        else:
            return '0' if self.colour == 'white' else '1'

    def __str__(self):
        row = 8 - self.row
        column = self.columns_str[self.column]
        return f'{column}{row}'

