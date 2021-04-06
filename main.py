from board import Board


def display_possible_moves(board, gui, clicked_square):
    valid_squares = board.get_piece_moves(clicked_square)
    gui.possible_squares(valid_squares)
    gui.update_display()
    return valid_squares


def main():
    board = Board(8, 8)
    whites_turn = True
    clicked_square = None
    while 1:
        if whites_turn:
            colour = "white"
        else:
            colour = "black"
        if not clicked_square:
            clicked_row, clicked_column = board.gui.event_listener()
            clicked_square = board.valid_piece(clicked_row, clicked_column, colour)
        valid_move = False
        if clicked_square:
            valid_squares = display_possible_moves(board, board.gui, clicked_square)
            updated_row, updated_column = board.gui.event_listener()
            new_clicked_square = board.valid_piece(updated_row, updated_column, colour)
            if not new_clicked_square:
                for square in valid_squares:
                    if square.row == updated_row and square.column == updated_column:
                        valid_move = True
                        board.update_board(clicked_square, square)
                        board.gui.clear_selection(valid_squares)
                        board.gui.draw_square(clicked_square)
                        if board.check and not board.checkmate:
                            print("CHECK")
                            orange_colour = (255, 140, 0)
                            board.gui.draw_square(square, colour=orange_colour)
                        if board.checkmate:
                            print("CHECKMATE!")
                            red_colour = (255, 0, 0)
                            board.gui.draw_square(square, colour=red_colour)
                        if board.stalemate:
                            print("STALEMATE!")
                            yellow_colour = (255, 255, 0)
                            board.gui.draw_square(square, colour=yellow_colour)
                        board.gui.draw_piece(square.piece.icon_asset, square)
                        board.gui.update_display()
                        break
                if valid_move:
                    whites_turn = not whites_turn
                    board.is_whites_turn = not board.is_whites_turn
                    clicked_square = None
                else:
                    board.gui.clear_selection(valid_squares)
                    board.gui.update_display()
                    clicked_square = new_clicked_square

            else:
                board.gui.clear_selection(valid_squares)
                board.gui.update_display()
                clicked_square = new_clicked_square


if __name__ == '__main__':
    main()
