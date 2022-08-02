import copy
from typing import List, Optional, Union
from chess_engine.square import Square
from chess_engine.pieces import Pawn, Bishop, Knight, Rook, Queen, King, Piece


class Board:
    def __init__(self):
        self.rows: int = 8
        self.columns: int = 8
        self.is_whites_turn: bool = True

        self.check, self.checkmate, self.stalemate = False, False, False
        self.chessboard, self.move_squares = [], []
        self.previous_move = None
        self.white_pieces, self.black_pieces = [], []
        self.all_possible_moves = []
        self.check_moves = {}
        self.promotion_piece = None
        self.piece_to_symbol = {
            Queen: "q",
            Bishop: "b",
            Knight: "n",
            Rook: "r",
            King: "k",
            Pawn: "p",
        }
        self.symbol_to_piece = {
            "q": Queen,
            "b": Bishop,
            "n": Knight,
            "r": Rook,
            "k": King,
            "p": Pawn,
        }
        self.pieces = {"white": {}, "black": {}}
        self._fen_repr = None
        self.fen_castling_status = None

    @property
    def fen_repr(self):
        return self._fen_repr

    @fen_repr.setter
    def fen_repr(self, fen_repr: str):
        self._fen_repr = fen_repr

    def get_chessboard(self) -> List[List[Square]]:
        return self.chessboard

    def initialise_board(self, parsed_fen_list: List = None) -> None:
        if not parsed_fen_list:
            parsed_fen_list = self.parse_fen(fen_str=self._fen_repr)
        for row in range(self.rows):
            current_row = []
            fen_row = parsed_fen_list[row]
            for column in range(self.columns):
                if (column + row) % 2 == 0:
                    colour = "white"
                else:
                    colour = "black"
                square = Square(row, column, colour)
                piece_symbol = fen_row[column]
                if piece_symbol.isupper():
                    piece_colour = "white"
                else:
                    piece_colour = "black"
                piece_type = self.symbol_to_piece.get(piece_symbol.lower())
                if piece_type:
                    square.piece = piece_type(row, column, piece_colour, piece_symbol)
                    if isinstance(square.piece, King):
                        if piece_colour == "white":
                            if "K" in self.fen_castling_status:
                                square.piece.castling_status.append("K")
                            if "Q" in self.fen_castling_status:
                                square.piece.castling_status.append("Q")
                        else:
                            if "k" in self.fen_castling_status:
                                square.piece.castling_status.append("k")
                            if "q" in self.fen_castling_status:
                                square.piece.castling_status.append("q")

                    piece_symbol = piece_symbol.lower()
                    if not self.pieces[piece_colour].get(piece_symbol):
                        self.pieces[piece_colour][piece_symbol] = [square.piece]
                    else:
                        self.pieces[piece_colour][piece_symbol].append(square.piece)
                current_row.append(square)
            self.chessboard.append(current_row)

    def get_move_squares(self) -> List[Square]:
        if not self.move_squares:
            return []
        return self.move_squares

    def clear_move_squares(self) -> None:
        self.move_squares.clear()

    def update_board(self, src_square: Square, dst_square: Square) -> None:
        self.is_whites_turn = not self.is_whites_turn
        self.check = self.__is_in_check(src_square=src_square, dst_square=dst_square)
        self.is_whites_turn = not self.is_whites_turn

        is_castle_move = self.__is_castle_move(
            src_square=src_square,
            dst_square=dst_square,
        )

        if is_castle_move:
            src_square.piece.castling_status.clear()

        if isinstance(src_square.piece, Rook) or isinstance(dst_square.piece, Rook):
            king_piece_colour = (
                dst_square.piece.colour
                if isinstance(dst_square.piece, Rook)
                else src_square.piece.colour
            )
            king_piece = self.pieces[king_piece_colour]["k"][0]
            if king_piece.castling_status:
                if src_square.piece.column > 4:
                    king_symbol = (
                        "K"
                        if self.is_whites_turn or king_piece_colour == "white"
                        else "k"
                    )
                    if king_symbol in king_piece.castling_status:
                        king_piece.castling_status.remove(king_symbol)
                else:
                    queen_symbol = (
                        "Q"
                        if self.is_whites_turn or king_piece_colour == "white"
                        else "q"
                    )
                    if queen_symbol in king_piece.castling_status:
                        king_piece.castling_status.remove(queen_symbol)

        en_passant_move = self.__is_en_passant_move(
            src_square=src_square, dst_square=dst_square, in_check=False
        )
        if en_passant_move:
            prev_src_square, prev_dst_square = self.previous_move
            en_passant_square = self.get_square(
                row=prev_dst_square.row, column=prev_dst_square.column
            )
            en_passant_square.piece = None
            self.move_squares.append(en_passant_square)

        if isinstance(src_square.piece, Pawn) and (
            dst_square.row == (self.rows - 1) or dst_square.row == 0
        ):
            self.__set_promoted_piece(
                src_square=src_square,
                dst_square=dst_square,
                piece_type=self.promotion_piece,
            )
        else:
            dst_square.piece = src_square.piece
        src_square.piece = None
        dst_square.piece.has_moved = True

        if (
            isinstance(dst_square.piece, Pawn)
            and abs(src_square.row - dst_square.row) == 2
        ):
            self.previous_move = [copy.copy(src_square), copy.copy(dst_square)]
        else:
            self.previous_move = None

        if (
            isinstance(dst_square.piece, King)
            and abs(src_square.column - dst_square.column) == 2
        ):
            if dst_square.column < (self.columns // 2):
                rook_square = self.get_square(row=dst_square.row, column=0)
                new_rook_square = self.get_square(
                    row=dst_square.row, column=dst_square.column + 1
                )
            else:
                rook_square = self.get_square(
                    row=dst_square.row, column=self.columns - 1
                )
                new_rook_square = self.get_square(
                    row=dst_square.row, column=dst_square.column - 1
                )
            new_rook_square.piece = rook_square.piece
            rook_square.piece = None
            self.move_squares.append(rook_square)

        dst_square.piece.has_moved = True

        if not self.check:
            return
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

    def __set_promoted_piece(
        self, src_square: Square, dst_square: Square, piece_type: Piece
    ) -> None:
        if not piece_type:
            piece_type = Queen

        piece_symbol = self.piece_to_symbol[piece_type]
        piece_symbol = piece_symbol.upper() if self.is_whites_turn else piece_symbol
        dst_square.piece = piece_type(
            dst_square.row, dst_square.column, src_square.piece.colour, piece_symbol
        )

    @staticmethod
    def __get_all_pieces(
        chessboard: List[List[Square]], colour: str = None
    ) -> List[Square]:
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
        is_promoted = False
        for move in square.piece.get_moves():
            possible_squares = self.__get_all_moves(src_square=square, move=move)
            if isinstance(square.piece, Pawn):
                for dst_square in possible_squares:
                    if square.piece.is_being_promoted(dst_row=dst_square.row):
                        promotion_pieces = [Queen, Bishop, Knight, Rook]
                        is_promoted = True
                        for promotion_piece in promotion_pieces:
                            moves.append([dst_square, promotion_piece])
            if not is_promoted:
                moves.extend(possible_squares)
        return moves

    def __get_all_moves(self, src_square, move) -> List[Square]:
        all_possible_moves = []
        is_in_check, is_starting_pawn, is_en_passant_move = False, False, False
        row, column = move
        dst_row = row + src_square.row
        dst_column = column + src_square.column

        while 1:
            if not self.__is_on_board(dst_row, dst_column):
                break

            dst_square = self.get_square(row=dst_row, column=dst_column)

            if self.__is_own_piece(src_square, dst_square):
                break

            is_capture_move = self.__is_capture_move(src_square, dst_square)

            if isinstance(src_square.piece, Pawn):
                is_en_passant_move = self.__is_en_passant_move(
                    src_square=src_square,
                    dst_square=dst_square,
                    in_check=is_in_check,
                )
                if is_en_passant_move:
                    is_capture_move = True

                if (not is_capture_move and column != 0) or (
                    is_capture_move and column == 0
                ):
                    break

                if (
                    not src_square.piece.has_moved
                    and column == 0
                    and abs(src_square.row - dst_square.row) < 3
                ):
                    is_starting_pawn = True
                else:
                    if not src_square.piece.has_moved and not is_capture_move:
                        break

            is_in_check = self.__is_in_check(
                src_square=src_square,
                dst_square=dst_square,
                is_en_passant_move=is_en_passant_move,
            )

            if not is_in_check:
                all_possible_moves.append(dst_square)

            if is_capture_move:
                break

            is_castle_move = self.__is_castle_move(src_square, dst_square, is_in_check)

            if (
                not src_square.piece.multi_moves
                and not is_castle_move
                and not is_starting_pawn
            ):
                break

            dst_row = row + dst_square.row
            dst_column = column + dst_square.column

        return all_possible_moves

    def __is_en_passant_move(
        self, src_square: Square, dst_square: Square, in_check: bool
    ) -> bool:
        if (
            not self.previous_move
            or in_check
            or src_square.column == dst_square.column
            or not isinstance(src_square.piece, Pawn)
        ):
            return False

        square_1, square_2 = self.previous_move

        if (
            square_2.column != dst_square.column
            or square_2.row != src_square.row
            or square_2.piece.colour == src_square.piece.colour
        ):
            return False
        return True

    def __is_castle_move(
        self, src_square: Square, dst_square: Square, in_check: bool = False
    ) -> bool:
        if (
            not isinstance(src_square.piece, King)
            or in_check
            or self.check
            or abs(src_square.row - dst_square.row) > 0
            or abs(src_square.column - dst_square.column > 1)
        ):
            return False

        castling_status = [_.lower() for _ in src_square.piece.castling_status]
        if not castling_status:
            return False

        if dst_square.column > 4 and "k" not in castling_status:
            return False

        if dst_square.column < 4 and "q" not in castling_status:
            return False

        if dst_square.column < 4:
            knight_column = 1
        else:
            knight_column = 6

        knight_square = self.get_square(row=src_square.row, column=knight_column)

        if knight_square.piece:
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

    def get_piece_square(self, row: int, column: int, colour: str) -> Optional[Square]:
        square = self.get_square(row=row, column=column)
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

    def __is_in_check(
        self,
        src_square: Square,
        dst_square: Square,
        is_en_passant_move: bool = False,
    ) -> bool:
        is_in_check = False
        dst_capture_piece = None
        en_passant_piece = None
        src_square_piece = src_square.piece
        if self.__is_capture_move(src_square, dst_square):
            dst_capture_piece = dst_square.piece

        if is_en_passant_move:
            prev_src_square, prev_dst_square = self.previous_move
            en_passant_square = self.get_square(
                row=prev_dst_square.row, column=prev_dst_square.column
            )
            en_passant_piece = en_passant_square.piece
            en_passant_square.piece = None

        if isinstance(src_square.piece, Pawn) and (
            dst_square.row == (self.rows - 1) or dst_square.row == 0
        ):
            piece_symbol = "Q" if self.is_whites_turn else "q"
            dst_square.piece = Queen(
                dst_square.row, dst_square.column, src_square.piece.colour, piece_symbol
            )
        else:
            dst_square.piece = src_square.piece
        src_square.piece = None

        colour = "white" if self.is_whites_turn else "black"
        squares = self.__get_all_pieces(
            chessboard=self.chessboard,
            colour=colour,
        )
        king_src_square = None
        knight_moves = []
        for square in squares:
            if isinstance(square.piece, King) and square.piece.colour == colour:
                king_src_square = square
            elif isinstance(square.piece, Knight):
                knight_moves = square.piece.moves

        for move in king_src_square.piece.moves:
            row, column = move
            dst_row = row + king_src_square.row
            dst_column = column + king_src_square.column

            while 1:
                if not self.__is_on_board(dst_row, dst_column):
                    break
                king_dst_square = self.get_square(row=dst_row, column=dst_column)

                if self.__is_own_piece(king_src_square, king_dst_square):
                    break

                if king_dst_square.piece:
                    if king_dst_square.piece.colour == king_src_square.piece.colour:
                        break

                    if (
                        isinstance(king_dst_square.piece, Pawn)
                        and abs(king_src_square.row - king_dst_square.row) < 2
                    ):
                        if abs(move[0] * move[1]) == 1:
                            if (
                                self.is_whites_turn
                                and king_src_square.row > king_dst_square.row
                            ):
                                is_in_check = True
                            if (
                                not self.is_whites_turn
                                and king_src_square.row < king_dst_square.row
                            ):
                                is_in_check = True
                        else:
                            break
                    elif isinstance(king_dst_square.piece, Queen):
                        is_in_check = True
                    elif isinstance(king_dst_square.piece, Rook) and (
                        king_src_square.column == king_dst_square.column
                        or king_src_square.row == king_dst_square.row
                    ):
                        is_in_check = True
                    elif isinstance(king_dst_square.piece, Bishop) and (
                        abs(move[0] * move[1]) == 1
                    ):
                        is_in_check = True
                    else:
                        break

                dst_row = row + king_dst_square.row
                dst_column = column + king_dst_square.column

        for move in knight_moves:
            row, column = move
            dst_row = row + king_src_square.row
            dst_column = column + king_src_square.column

            if not self.__is_on_board(dst_row, dst_column):
                continue
            king_dst_square = self.get_square(row=dst_row, column=dst_column)

            if self.__is_own_piece(king_src_square, king_dst_square):
                continue

            if king_dst_square.piece:
                if king_dst_square.piece.colour != king_src_square.piece.colour:
                    if isinstance(king_dst_square.piece, Knight):
                        is_in_check = True

        src_square.piece = src_square_piece
        if dst_capture_piece:
            dst_square.piece = dst_capture_piece
        else:
            dst_square.piece = None

        if en_passant_piece:
            en_passant_square.piece = en_passant_piece

        if is_in_check:
            piece_str = str(src_square)
            if piece_str not in self.check_moves:
                self.check_moves[piece_str] = []
            self.check_moves[piece_str].append((dst_square.row, dst_square.column))

        return is_in_check

    def get_all_possible_moves(self) -> List[List[Union[Square, List[Square]]]]:
        pieces = self.__get_all_pieces(
            chessboard=self.chessboard,
            colour="white" if self.is_whites_turn else "black",
        )
        all_possible_moves = []
        for square in pieces:
            possible_moves = self.get_piece_moves(square)
            if possible_moves:
                all_possible_moves.append([square, possible_moves])
        self.all_possible_moves = all_possible_moves
        return all_possible_moves

    def get_board_value(self) -> int:
        pieces = self.__get_all_pieces(chessboard=self.chessboard)
        total_white = 0
        total_black = 0
        for square in pieces:
            if square.piece.colour == "white":
                total_white += square.piece.value
            else:
                total_black += square.piece.value
        if self.is_whites_turn:
            return total_white - total_black
        else:
            return total_black - total_white

    def __repr__(self):
        chess_board_str = ""
        for row in self.chessboard:
            chess_board_str += f"{str([str(piece) for piece in row])}\n"
        return chess_board_str

    def get_fen_representation(self) -> List[List[str]]:
        fen_list = []
        for row in self.chessboard:
            fen_list.append(
                [str(square.piece) if square.piece else repr(square) for square in row]
            )
        return fen_list

    def get_fen(self) -> str:
        fen = ""

        for row_index, row in enumerate(self.chessboard):
            empty_square_count = 0
            for square in row:
                if square.piece:
                    if empty_square_count > 0:
                        fen += str(empty_square_count)
                        empty_square_count = 0
                    fen += str(square.piece)
                else:
                    empty_square_count += 1
            if empty_square_count > 0:
                fen += str(empty_square_count)
            if row_index == 7:
                if self.is_whites_turn:
                    fen += " w"
                else:
                    fen += " b"
                castling_stat = self.get_castling_status()
                castling_str = ""
                for element in castling_stat:
                    castling_str += element
                fen += f" {castling_str}"
            else:
                fen += "/"
        return fen

    def get_castling_status(self) -> List:
        black_king = self.pieces["black"]["k"][0]
        white_king = self.pieces["white"]["k"][0]

        return white_king.castling_status + black_king.castling_status

    def parse_fen(self, fen_str: str) -> List[List[str]]:
        fen_str = fen_str.replace(" ", "/")
        fen_list = fen_str.split("/")
        board_rep = fen_list[:8]
        if len(fen_list) > 9:
            self.fen_castling_status = fen_list[9:][0]
        else:
            self.fen_castling_status = []
        turn = fen_list[8]
        if turn == "w":
            self.is_whites_turn = True
        else:
            self.is_whites_turn = False
        parsed_fen_list = []
        for row in board_rep:
            parsed_col_list = []
            for col in row:
                if col.isdigit():
                    chr_list = int(col) * ["x"]
                    parsed_col_list.extend(chr_list)
                else:
                    parsed_col_list.extend(col)
            parsed_fen_list.append(parsed_col_list)
        return parsed_fen_list

    def moves_to_str(self, moves) -> List[str]:
        moves_str = []
        for move in moves:
            src_square, dst_squares = move
            for dst in dst_squares:
                if isinstance(dst, List):
                    dst_square, piece_type = dst
                    piece = self.piece_to_symbol[piece_type]
                    dst = f"{dst_square}{piece}"
                moves_str.append(f"{src_square}{dst}")
        return moves_str
