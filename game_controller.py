from board import Board
from ai import AI
import copy
import sys


class GameController(object):
    def __init__(self):
        self.board = Board(8, 8)
        self.ai = AI()
        self.whites_turn = True
        self.clicked_square = None

    def human_move(self):
        valid_move = False
        if self.whites_turn:
            colour = "white"
        else:
            colour = "black"
        if not self.clicked_square:
            clicked_row, clicked_column = self.board.gui.event_listener()
            self.clicked_square = self.board.is_valid_piece(clicked_row, clicked_column, colour)
        if self.clicked_square:
            valid_squares = self.display_possible_moves()
            updated_row, updated_column = self.board.gui.event_listener()
            new_clicked_square = self.board.is_valid_piece(updated_row, updated_column, colour)
            if not new_clicked_square:
                for square in valid_squares:
                    if square.row == updated_row and square.column == updated_column:
                        valid_move = True
                        self.update_game_state(
                            src_square=self.clicked_square,
                            dst_square=square,
                            valid_squares=valid_squares
                        )
                        self.clicked_square = None
                        break
            if new_clicked_square or not valid_move:
                self.board.gui.clear_selection(valid_squares)
                self.board.gui.update_display()
                self.clicked_square = new_clicked_square
                self.human_move()

    def ai_move(self):
        move = self.ai.move(
            white_move=self.whites_turn,
            board=self.board
        )
        src_square, dst_square = move
        self.update_game_state(
            src_square=src_square,
            dst_square=dst_square,
            valid_squares=[dst_square]
        )

    def update_game_state(self, src_square, dst_square, valid_squares):
        self.board.update_board(src_square, dst_square)
        self.board.gui.clear_selection(valid_squares)
        self.board.gui.draw_square(src_square)
        if self.board.check and not self.board.checkmate:
            print("CHECK")
            orange_colour = (255, 140, 0)
            self.board.gui.draw_square(
                dst_square,
                colour=orange_colour
            )
        if self.board.checkmate:
            print('CHECKMATE!')
            if self.whites_turn:
                print('White wins!')
            else:
                print('Black wins!')
            red_colour = (255, 0, 0)
            self.board.gui.draw_square(
                dst_square,
                colour=red_colour
            )
            # sys.exit(0)
        if self.board.stalemate:
            print("STALEMATE!")
            yellow_colour = (255, 255, 0)
            self.board.gui.draw_square(
                dst_square,
                colour=yellow_colour
            )
            # sys.exit(0)
        self.board.gui.draw_piece(
            dst_square.piece.icon_asset,
            dst_square
        )
        self.board.gui.update_display()
        self.board.previous_move = [copy.copy(src_square), copy.copy(dst_square)]
        if self.board.en_passant_capture_square:
            self.board.en_passant_capture_square.clear()
        self.whites_turn = not self.whites_turn
        self.board.is_whites_turn = not self.board.is_whites_turn

    def display_possible_moves(self):
        valid_squares = self.board.get_piece_moves(self.clicked_square)
        self.board.gui.possible_squares(valid_squares)
        self.board.gui.update_display()
        return valid_squares
