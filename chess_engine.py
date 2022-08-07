from chess_engine.backend.game_controller import GameController
from chess_engine.backend.board import Board
from chess_engine.backend.ai import AI
from chess_engine.frontend.user_interface import GUI


def initialise_game() -> GameController:
    board_obj = Board()
    board_obj.fen_repr = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
    return game_controller_obj


def start_game(game_controller_obj: GameController):
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
    game_controller_obj = initialise_game()
    start_game(game_controller_obj=game_controller_obj)


if __name__ == "__main__":
    main()
