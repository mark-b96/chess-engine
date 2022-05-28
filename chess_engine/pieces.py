from copy import deepcopy


class Piece:
    def __init__(self, row, column, colour):
        self.row: int = row
        self.column: int = column
        self.colour: str = colour
        self.multi_moves = False
        self.icon_asset = None

        if self.colour == "white":
            self.colour_code = (255, 255, 255, 0)
        else:
            self.colour_code = (0, 0, 0, 0)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        skip_classes: set = {'icon_asset'}
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in skip_classes:
                setattr(result, k, deepcopy(v, memo))
        return result


class Pawn(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        if self.row < 2:
            self.moves = [[1, 0], [1, 1], [1, -1]]
        else:
            self.moves = [[-1, 0], [-1, 1], [-1, -1]]

        self.has_moved = False
        self.value = 1

    def __repr__(self):
        if self.colour == "white":
            return 'P'
        else:
            return 'p'


class Knight(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        self.moves = [[2, 1], [1, 2], [-2, 1], [-2, -1], [2, -1], [-1, 2], [-1, -2], [1, -2]]
        self.value = 3

    def __repr__(self):
        if self.colour == "white":
            return 'N'
        else:
            return 'n'


class Bishop(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        self.moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        self.multi_moves = True
        self.value = 3

    def __repr__(self):
        if self.colour == "white":
            return 'B'
        else:
            return 'b'


class Rook(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        self.moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.multi_moves = True
        self.has_moved = False
        self.value = 5

    def __repr__(self):
        if self.colour == "white":
            return 'R'
        else:
            return 'r'


class Queen(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        self.moves = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        self.multi_moves = True
        self.value = 9

    def __repr__(self):
        if self.colour == "white":
            return 'Q'
        else:
            return 'q'


class King(Piece):
    def __init__(self, row, column, colour):
        super().__init__(row, column, colour)
        self.moves = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        self.has_moved = False
        self.in_check = False
        self.has_castled = False
        self.value = 0

    def __repr__(self):
        if self.colour == "white":
            return 'K'
        else:
            return 'k'
