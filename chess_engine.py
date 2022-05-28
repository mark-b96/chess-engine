from chess_engine.game_controller import GameController
from chess_engine.board import Board
from chess_engine.ai import AI
from chess_engine.user_interface import GUI
import time


def start_game():
    board_size = 8
    board_obj = Board(
        rows=board_size,
        columns=board_size,
    )
    board_obj.initialise_board()

    gui_obj = GUI(
        board_size=board_size,
        square_size=100,
    )

    ai_obj = AI()

    game_controller_obj = GameController(
        ai_obj=ai_obj,
        board_obj=board_obj,
        gui_obj=gui_obj,
    )
    game_controller_obj.draw_game_board()

    while 1:
        game_controller_obj.ai_move()
        if game_controller_obj.board_obj.checkmate or game_controller_obj.board_obj.stalemate:
            break
        game_controller_obj.ai_move()
        if game_controller_obj.board_obj.checkmate or game_controller_obj.board_obj.stalemate:
            break


def main():
    start_game()


if __name__ == '__main__':
    main()
