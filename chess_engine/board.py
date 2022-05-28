import copy
from copy import deepcopy
from typing import List, Optional, Union
from chess_engine.square import Square
from chess_engine.pieces import Pawn, Bishop, Knight, Rook, Queen, King


class Board:
    def __init__(self, rows, columns):
        self.rows: int = rows
        self.columns: int = columns
        self.is_whites_turn: bool = True

        self.check, self.checking_for_check, self.checkmate, self.stalemate = False, False, False, False
        self.chessboard, self.move_squares = [], []
        self.previous_move = None
        self.current_move = None

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def get_chessboard(self) -> List[List]:
        return self.chessboard

    def initialise_board(self) -> None:
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if (column + row) % 2 == 0:
                    colour = "white"
                else:
                    colour = "black"
                square = Square(row, column, colour)
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
                current_row.append(square)
            self.chessboard.append(current_row)

    def get_move_squares(self) -> List[Square]:
        if not self.move_squares:
            return []
        return self.move_squares

    def clear_move_squares(self) -> None:
        self.move_squares.clear()

    def update_board(self, src_square: Square, dst_square: Square) -> None:
        self.current_move = [copy.deepcopy(src_square), copy.deepcopy(dst_square)]
        self.is_whites_turn = not self.is_whites_turn
        self.check = self.__is_in_check(
            src_square=src_square,
            dst_square=dst_square
        )
        self.is_whites_turn = not self.is_whites_turn

        en_passant_move = self.__is_en_passant_move(
            src_square=src_square,
            dst_square=dst_square,
            in_check=False
        )
        if en_passant_move:
            prev_src_square, prev_dst_square = self.previous_move
            en_passant_square = self.get_square(
                row=prev_dst_square.row,
                column=prev_dst_square.column
            )
            en_passant_square.piece = None
            self.move_squares.append(en_passant_square)

        if isinstance(src_square.piece, Pawn) and \
                (dst_square.row == (self.rows - 1) or dst_square.row == 0):
            dst_square.piece = Queen(dst_square.row, dst_square.column, src_square.piece.colour)
        else:
            dst_square.piece = src_square.piece
        src_square.piece = None
        dst_square.piece.has_moved = True

        if isinstance(dst_square.piece, Pawn) and abs(src_square.row - dst_square.row) == 2:
            self.previous_move = [copy.copy(src_square), copy.copy(dst_square)]
        else:
            self.previous_move = None

        if isinstance(dst_square.piece, King) and abs(src_square.column - dst_square.column) == 2:
            if dst_square.column < (self.columns // 2):
                rook_square = self.get_square(
                    row=dst_square.row,
                    column=0
                )
                new_rook_square = self.get_square(
                    row=dst_square.row,
                    column=dst_square.column + 1
                )
            else:
                rook_square = self.get_square(
                    row=dst_square.row,
                    column=self.columns - 1
                )
                new_rook_square = self.get_square(
                    row=dst_square.row,
                    column=dst_square.column - 1
                )
            new_rook_square.piece = rook_square.piece
            rook_square.piece = None
            self.move_squares.append(rook_square)

        colour = "black" if self.is_whites_turn else "white"
        squares = self.__get_all_pieces(
            chessboard=self.chessboard,
            colour=colour,
        )

        all_possible_squares = []
        self.is_whites_turn = not self.is_whites_turn
        for square in squares:
            possible_squares = self.get_piece_moves(square)
            all_possible_squares.append(possible_squares)
        self.is_whites_turn = not self.is_whites_turn

        if not any(all_possible_squares):
            if self.check:
                self.checkmate = True
            else:
                self.stalemate = True

    @staticmethod
    def __get_all_pieces(chessboard: List[List[Square]], colour: str = None) -> List[Square]:
        squares = []
        for row in chessboard:
            for square in row:
                if not square.piece:
                    continue
                if square.piece.colour != colour and colour:
                    continue
                squares.append(square)
        return squares

    def get_piece_moves(self, square: Square) -> List[Square]:
        moves = []
        for move in square.piece.moves:
            possible_squares = self.__get_all_moves(move, square, square, [])
            moves.extend(possible_squares)
        return moves

    def __get_all_moves(
            self,
            move: List,
            src_square: Square,
            dst_square: Square,
            possible_moves: List
    ) -> List[Square]:
        in_check = False
        row, column = move
        dst_row = row + dst_square.row
        dst_column = column + dst_square.column

        if not self.__is_on_board(dst_row, dst_column):
            return possible_moves

        dst_square = self.get_square(
            row=dst_row,
            column=dst_column
        )

        if self.__is_own_piece(src_square, dst_square):
            return possible_moves

        if not self.checking_for_check:
            in_check = self.__is_in_check(src_square, dst_square)

        if not isinstance(src_square.piece, Pawn):
            if not in_check:
                possible_moves.append(dst_square)
            if not self.__is_capture_move(src_square, dst_square):
                can_castle = self.__is_castle_move(src_square, dst_square, in_check)
                if src_square.piece.multi_moves or can_castle:
                    self.__get_all_moves(move, src_square, dst_square, possible_moves)
            return possible_moves

        is_en_passant_move = self.__is_en_passant_move(
            src_square=src_square,
            dst_square=dst_square,
            in_check=in_check,
        )
        if is_en_passant_move and not in_check:
            possible_moves.append(dst_square)

        if self.__is_capture_move(src_square, dst_square) and column != 0 and not in_check:
            possible_moves.append(dst_square)
        if not self.__is_capture_move(src_square, dst_square) and column == 0:
            if not in_check:
                possible_moves.append(dst_square)
            if not src_square.piece.has_moved and abs(src_square.row - dst_square.row) < 2:
                self.__get_all_moves(move, src_square, dst_square, possible_moves)

        return possible_moves

    def __is_en_passant_move(self, src_square: Square, dst_square: Square, in_check: bool) -> bool:
        if not self.previous_move or in_check or \
                src_square.column == dst_square.column or \
                not isinstance(src_square.piece, Pawn):
            return False

        square_1, square_2 = self.previous_move

        if square_2.column != dst_square.column or \
                square_2.row != src_square.row or \
                square_2.piece.colour == src_square.piece.colour:
            return False
        return True

    def __is_castle_move(self, src_square: Square, dst_square: Square, in_check) -> bool:
        if not isinstance(src_square.piece, King) or \
                abs(src_square.column - dst_square.column) > 1 or \
                in_check:
            return False

        if dst_square.column < (self.columns // 2):
            corner_column = 0
            knight_square = self.get_square(
                row=src_square.row,
                column=1
            )
            if knight_square.piece is not None:
                return False
        else:
            corner_column = self.columns - 1

        corner_square = self.get_piece(
            row=dst_square.row,
            column=corner_column,
            colour="white" if self.is_whites_turn else "black"
        )
        if not corner_square:
            return False

        if not isinstance(corner_square.piece, Rook) or \
                src_square.piece.has_moved or \
                src_square.piece.has_castled or \
                corner_square.piece.has_moved:
            return False

        return True

    @staticmethod
    def __is_capture_move(src_square: Square, dst_square: Square) -> bool:
        if dst_square.piece:
            if dst_square.piece.colour != src_square.piece.colour:
                return True
        return False

    def __is_on_board(self, row: int, column: int) -> bool:
        if (-1 < row < self.rows) and (-1 < column < self.columns):
            return True
        return False

    def get_piece(self, row: int, column: int, colour: str) -> Optional[Square]:
        square = self.get_square(
            row=row,
            column=column
        )
        if not square.piece:
            return None
        if square.piece.colour == colour:
            return square

    def get_square(self, row: int, column: int) -> Square:
        return self.chessboard[row][column]

    @staticmethod
    def __is_own_piece(src_square: Square, dst_square: Square) -> bool:
        if dst_square.piece:
            if dst_square.piece.colour == src_square.piece.colour:
                return True
        return False

    def __is_in_check(self, src_square: Square, dst_square: Square) -> bool:
        self.checking_for_check = True
        is_in_check = False
        dst_capture_piece = None
        is_capture_move = self.__is_capture_move(src_square, dst_square)
        if is_capture_move:
            dst_capture_piece = dst_square.piece

        if isinstance(src_square.piece, Pawn) and \
                (dst_square.row == (self.rows - 1) or dst_square.row == 0):
            dst_square.piece = Queen(dst_square.row, dst_square.column, src_square.piece.colour)
        else:
            dst_square.piece = src_square.piece
        src_square.piece = None

        colour = "black" if self.is_whites_turn else "white"
        squares = self.__get_all_pieces(
            chessboard=self.chessboard,
            colour=colour,
        )

        self.is_whites_turn = not self.is_whites_turn
        for square in squares:
            possible_squares = self.get_piece_moves(square)
            for possible_square in possible_squares:
                if isinstance(possible_square.piece, King):
                    is_in_check = True
        self.is_whites_turn = not self.is_whites_turn

        src_square.piece = dst_square.piece
        if dst_capture_piece:
            dst_square.piece = dst_capture_piece
        else:
            dst_square.piece = None

        self.checking_for_check = False
        return is_in_check

    def get_all_possible_moves(self) -> List[List[Union[Square, List[Square]]]]:
        pieces = self.__get_all_pieces(
            chessboard=self.chessboard,
            colour="white" if self.is_whites_turn else "black"
        )
        all_possible_moves = []
        for square in pieces:
            possible_moves = self.get_piece_moves(square)
            if possible_moves:
                all_possible_moves.append([square, possible_moves])
        return all_possible_moves

    def get_board_value(self):
        pieces = self.__get_all_pieces(chessboard=self.chessboard)
        total_white = 0
        total_black = 0
        for square in pieces:
            if square.piece.colour == 'white':
                total_white += square.piece.value
            else:
                total_black += square.piece.value
        if self.is_whites_turn:
            return total_white - total_black
        else:
            return total_black - total_white

    def __repr__(self):
        chess_board_str = ''
        for row in self.chessboard:
            chess_board_str += f"{str([str(piece) for piece in row])}\n"
        return chess_board_str
