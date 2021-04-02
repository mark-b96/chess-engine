import copy
from user_interface import GUI


class Board(object):
    def __init__(self, _rows: int, _columns: int):
        self.rows = _rows
        self.columns = _columns
        self.chessboard = []
        self.gui = GUI(800, 800)
        self.check = False
        self.checking_for_check = False
        self.castling = False
        self.black_pieces, self.white_pieces = [], []
        self.initialise_board()
        self.gui.update_display()

    def initialise_board(self):
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if (column + row) % 2 == 0:
                    colour = "white"
                else:
                    colour = "black"
                square = Square(row, column, colour)
                self.gui.draw_square(square)
                piece_colour = "black"
                if row > 5:
                    piece_colour = "white"
                if row == 1 or row == 6:
                    square.piece = Pawn(row, column, piece_colour)
                if row < 1 or row > 6:
                    if column == 0 or column == 7:
                        square.piece = Rook(row, column, piece_colour)
                    if column == 1 or column == 6:
                        square.piece = Knight(row, column, piece_colour)
                    if column == 2 or column == 5:
                        square.piece = Bishop(row, column, piece_colour)
                    if column == 3:
                        square.piece = Queen(row, column, piece_colour)
                    if column == 4:
                        square.piece = King(row, column, piece_colour)
                if square.piece:
                    piece_icon = self.gui.load_piece(square)
                    self.gui.draw_piece(piece_icon, square)
                    square.piece.icon_asset = piece_icon
                    if square.piece.colour == "black":
                        self.black_pieces.append(square)
                    else:
                        self.white_pieces.append(square)
                current_row.append(square)
            self.chessboard.append(current_row)

    def update_board(self, src_square, dst_square):
        if dst_square.piece:
            if dst_square.piece.colour != src_square.piece.colour:
                if src_square.piece.colour == "white":
                    self.black_pieces.remove(dst_square)
                else:
                    self.white_pieces.remove(dst_square)
        if type(src_square.piece) == Pawn and (dst_square.row == 7 or dst_square.row == 0):
            dst_square.piece = Queen(dst_square.row, dst_square.column, src_square.piece.colour)
            piece_icon = self.gui.load_piece(dst_square)
            self.gui.draw_piece(piece_icon, dst_square)
            dst_square.piece.icon_asset = piece_icon
        else:
            dst_square.piece = src_square.piece

        if dst_square.piece.colour == "white":
            self.white_pieces.append(dst_square)
            self.white_pieces.remove(src_square)
        else:
            self.black_pieces.append(dst_square)
            self.black_pieces.remove(src_square)
        src_square.piece = None
        dst_square.piece.row = dst_square.row
        dst_square.piece.column = dst_square.column
        if self.castling:
            dst_square.piece.has_castled = True
            # if dst_square.column == 6:
            #     src_rook_square = self.black_pieces
            #     dst_rook_square = self.chessboard[dst_square.row][5]
            #     dst_rook_square.piece = src_rook_square.piece
            #     src_rook_square.piece = None
            #     dst_square.piece.row = dst_square.row
            #     dst_square.piece.column = dst_square.column

    def get_piece_moves(self, square):
        moves = []
        for move in square.piece.moves:
            multi_moves = square.piece.multi_moves
            possible_squares = self.get_all_moves(move, square, square, [], multi_moves)
            for updated_square in possible_squares:
                moves.append(updated_square)
        return moves

    def get_all_moves(self, move, src_square, square, possible_moves, multi_moves) -> list:
        in_check = False
        row, column = move
        updated_row = row + square.row
        updated_column = column + square.column
        if self.on_board(updated_row, updated_column):
            updated_square = self.chessboard[updated_row][updated_column]
            if not self.own_piece(src_square, updated_square):
                if not self.checking_for_check:
                    in_check = self.in_check(src_square, updated_square)
                if type(src_square.piece) == Pawn:
                    if column != 0:
                        if self.capture_move(src_square, updated_square) and not in_check:
                            possible_moves.append(updated_square)
                    else:
                        if not self.capture_move(src_square, updated_square) and not in_check:
                            possible_moves.append(updated_square)
                            if (square.row == 6 and square.piece.colour == "white") or \
                                    (square.row == 1 and square.piece.colour == "black"):
                                self.get_all_moves(move, src_square, updated_square, possible_moves, multi_moves)
                else:
                    if not in_check:
                        possible_moves.append(updated_square)
                    if not self.capture_move(src_square, updated_square) and not in_check:
                        can_castle = self.castle_move(src_square, updated_square, row, column)
                        if multi_moves or can_castle:
                            self.get_all_moves(move, src_square, updated_square, possible_moves, multi_moves)
        return possible_moves

    def castle_move(self, src_square, dst_square, row, column):
        if type(src_square.piece) == King and row == 0 and abs(column) == 1 and dst_square.column > 2:
            if not src_square.piece.has_moved and not src_square.piece.has_castled:
                self.castling = True
                return True
        return False

    @staticmethod
    def capture_move(src_square, dst_square) -> bool:
        if dst_square.piece:
            if dst_square.piece.colour != src_square.piece.colour:
                return True
        return False

    def on_board(self, row: int, column: int) -> bool:
        if (-1 < row < self.rows) and (-1 < column < self.columns):
            return True
        return False

    def valid_piece(self, row: int, column: int, colour: str) -> object:
        square = self.chessboard[row][column]
        if square.piece:
            if square.piece.colour == colour:
                return square
        return None

    @staticmethod
    def own_piece(original_square, target_square) -> bool:
        if target_square.piece:
            if target_square.piece.colour == original_square.piece.colour:
                return True
        return False

    def in_check(self, src_square, dst_square) -> bool:
        self.checking_for_check = True
        is_in_check = False
        src_square_colour = src_square.piece.colour
        src_piece_copy = copy.copy(src_square.piece)
        dst_piece_copy = copy.copy(dst_square.piece)
        white_pieces_copy = self.white_pieces.copy()
        black_pieces_copy = self.black_pieces.copy()
        self.update_board(src_square, dst_square)
        squares = self.white_pieces if src_square_colour == "black" else self.black_pieces

        for square in squares:
            possible_squares = self.get_piece_moves(square)
            for possible_square in possible_squares:
                if type(possible_square.piece) == King:
                    is_in_check = True

        src_square.piece = src_piece_copy
        dst_square.piece = dst_piece_copy
        self.white_pieces = white_pieces_copy
        self.black_pieces = black_pieces_copy
        self.checking_for_check = False
        return is_in_check


class Square(object):
    def __init__(self, _row: int, _column: int, _colour: str):
        self.colour = _colour
        self.row = _row
        self.column = _column
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
        if self.row < 3:
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
