

class GameController:
    def __init__(self, ai_obj, board_obj, gui_obj):
        self.ai_obj = ai_obj
        self.board_obj = board_obj
        self.gui_obj = gui_obj

    def draw_game_board(self) -> None:
        chessboard = self.board_obj.get_chessboard()
        for row in chessboard:
            for square in row:
                self.gui_obj.draw_square(square)
                if square.piece:
                    piece_icon = self.gui_obj.load_piece(square)
                    self.gui_obj.draw_piece(piece_icon, square)
                    square.piece.icon_asset = piece_icon
        self.gui_obj.update_display()

    def get_src_square(self):
        clicked_row, clicked_column = self.gui_obj.event_listener()
        src_square = self.board_obj.get_piece(
            row=clicked_row,
            column=clicked_column,
            colour="white" if self.board_obj.is_whites_turn else "black"
        )
        return src_square

    def get_dst_square(self, valid_squares: list):
        clicked_row, clicked_column = self.gui_obj.event_listener()
        dst_square = self.board_obj.get_square(
            row=clicked_row,
            column=clicked_column
        )
        if dst_square not in valid_squares:
            dst_square = self.board_obj.get_piece(
                row=clicked_row,
                column=clicked_column,
                colour="white" if self.board_obj.is_whites_turn else "black"
            )
        return dst_square

    def human_move(self):
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

    def ai_move(self):
        move = self.ai_obj.get_optimal_move(board=self.board_obj)
        src_square, dst_square, promotion_piece = move
        self.update_game_state(
            src_square=src_square,
            dst_square=dst_square,
            valid_squares=[dst_square],
            promotion_piece=promotion_piece
        )

    def update_game_state(self, src_square, dst_square, valid_squares: list, promotion_piece=None) -> None:
        if promotion_piece:
            self.board_obj.promotion_piece = promotion_piece
        self.board_obj.update_board(src_square, dst_square)
        valid_squares.extend(self.board_obj.get_move_squares())
        self.board_obj.clear_move_squares()

        if not dst_square.piece.icon_asset:
            piece_icon = self.gui_obj.load_piece(dst_square)
            dst_square.piece.icon_asset = piece_icon
        self.gui_obj.clear_selection(valid_squares)
        self.gui_obj.draw_square(src_square)

        if self.board_obj.checkmate:
            print('CHECKMATE!')
            if self.board_obj.is_whites_turn:
                print('White wins!')
            else:
                print('Black wins!')
            red_colour = (255, 0, 0)
            self.gui_obj.draw_square(
                dst_square,
                colour=red_colour
            )
        elif self.board_obj.stalemate:
            print("STALEMATE!")
            yellow_colour = (255, 255, 0)
            self.gui_obj.draw_square(
                dst_square,
                colour=yellow_colour
            )
        elif self.board_obj.check:
            print("CHECK")
            orange_colour = (255, 140, 0)
            self.gui_obj.draw_square(
                dst_square,
                colour=orange_colour
            )

        self.gui_obj.draw_piece(
            dst_square.piece.icon_asset,
            dst_square
        )
        self.gui_obj.update_display()
        self.board_obj.is_whites_turn = not self.board_obj.is_whites_turn

    def display_possible_moves(self, valid_squares: list) -> None:
        self.gui_obj.possible_squares(valid_squares)
        self.gui_obj.update_display()
