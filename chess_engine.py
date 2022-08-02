from chess_engine.game_controller import GameController
from chess_engine.board import Board
from chess_engine.ai import AI
from chess_engine.user_interface import GUI


def start_game():
    board_obj = Board()
    board_obj.fen_repr = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
    board_obj.initialise_board()

    gui_obj = GUI(
        board_size=8,
        square_size=100,
    )
    gui_obj.draw_game_board(chessboard=board_obj.chessboard)

    ai_obj = AI()

    game_controller_obj = GameController(
        ai_obj=ai_obj,
        board_obj=board_obj,
        gui_obj=gui_obj,
    )

    while 1:
        game_controller_obj.human_move()
        if (
            game_controller_obj.board_obj.checkmate
            or game_controller_obj.board_obj.stalemate
        ):
            break
        game_controller_obj.ai_move()
        if (
            game_controller_obj.board_obj.checkmate
            or game_controller_obj.board_obj.stalemate
        ):
            break


def main():
    start_game()


if __name__ == "__main__":
    main()
