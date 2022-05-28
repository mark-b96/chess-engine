
class Square:
    def __init__(self, row, column, colour):
        self.row: int = row
        self.column: int = column
        self.colour: str = colour
        self.piece = None
        if self.colour == 'white':
            self.colour_code = (0, 128, 128)
        else:
            self.colour_code = (21, 71, 52)

    def __repr__(self):
        if self.piece:
            return self.piece.__repr__()
        else:
            return '0' if self.colour == 'white' else '1'

