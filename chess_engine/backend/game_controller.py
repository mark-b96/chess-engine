from loguru import logger
from typing import List

from chess_engine.backend.square import Square
from chess_engine.backend.pieces import Piece


class GameController:
    def __init__(self, ai_obj, board_obj, gui_obj):
        self.ai_obj = ai_obj
        self.board_obj = board_obj
        self.gui_obj = gui_obj

    def get_src_square(self) -> Square:
        clicked_row, clicked_column = self.gui_obj.event_listener()
        src_square = self.board_obj.get_piece_square(
            row=clicked_row,
            column=clicked_column,
            colour="white" if self.board_obj.is_whites_turn else "black",
        )
        return src_square

    def get_dst_square(self, valid_squares: List[Square]) -> Square:
        clicked_row, clicked_column = self.gui_obj.event_listener()
        dst_square = self.board_obj.get_square(row=clicked_row, column=clicked_column)
        if dst_square not in valid_squares:
            dst_square = self.board_obj.get_piece_square(
                row=clicked_row,
                column=clicked_column,
                colour="white" if self.board_obj.is_whites_turn else "black",
            )
        return dst_square

    def human_move(self) -> None:
        src_square, dst_square, valid_squares = None, None, None

        while not dst_square:
            while not src_square:
                src_square = self.get_src_square()
            valid_squares = self.board_obj.get_piece_moves(src_square)
            valid_squares = [
                square if not isinstance(square, list) else square[0]
                for square in valid_squares
            ]
            self.display_possible_moves(valid_squares)

            dst_square = self.get_dst_square(valid_squares)

            if dst_square and dst_square not in valid_squares:
                if dst_square.piece:
                    src_square = dst_square
                dst_square = None
            self.gui_obj.clear_selection(valid_squares)

        self.update_game_state(
            src_square=src_square,
            dst_square=dst_square,
            valid_squares=valid_squares,
        )

    def ai_move(self) -> None:
        move = self.ai_obj.get_optimal_move(board=self.board_obj)
        src_square, dst_square, promotion_piece = move
        self.update_game_state(
            src_square=src_square,
            dst_square=dst_square,
            valid_squares=[dst_square],
            promotion_piece=promotion_piece,
        )

    def update_game_state(
        self,
        src_square: Square,
        dst_square: Square,
        valid_squares: List[Square],
        promotion_piece: Piece = None,
    ) -> None:
        if promotion_piece:
            self.board_obj.promotion_piece = promotion_piece
        self.board_obj.update_board(src_square=src_square, dst_square=dst_square)
        valid_squares.extend(self.board_obj.get_move_squares())
        self.board_obj.clear_move_squares()

        self.gui_obj.update_squares(
            src_square=src_square, dst_square=dst_square, valid_squares=valid_squares
        )

        if self.board_obj.checkmate:
            logger.info("Checkmate!")
            if self.board_obj.is_whites_turn:
                logger.info("White Wins!")
            else:
                logger.info("Black Wins!")
            self.gui_obj.draw_square(dst_square, colour_str="red")
        elif self.board_obj.stalemate:
            logger.info("Stalemate!")
            self.gui_obj.draw_square(dst_square, colour_str="yellow")
        elif self.board_obj.check:
            logger.info("Check!")
            self.gui_obj.draw_square(dst_square, colour_str="orange")

        self.gui_obj.draw_piece(dst_square.piece.icon_asset, dst_square)
        self.gui_obj.update_display()
        self.board_obj.is_whites_turn = not self.board_obj.is_whites_turn

    def display_possible_moves(self, valid_squares: List[Square]) -> None:
        self.gui_obj.possible_squares(valid_squares)
        self.gui_obj.update_display()
