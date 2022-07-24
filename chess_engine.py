from chess_engine.game_controller import GameController
from chess_engine.board import Board
from chess_engine.ai import AI
from chess_engine.user_interface import GUI
import time
import sys


def start_game():
    board_obj = Board()
    # board_obj.fen_repr = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ"
    # board_obj.fen_repr = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq"
    # board_obj.fen_repr = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w"
    # board_obj.fen_repr = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w"
    # board_obj.fen_repr = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq"
    # board_obj.fen_repr = "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ"
    board_obj.fen_repr = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
    board_obj.initialise_board()

    gui_obj = GUI(
        board_size=8,
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
        # sys.exit()
        game_controller_obj.human_move()
        if game_controller_obj.board_obj.checkmate or game_controller_obj.board_obj.stalemate:
            break


def main():
    start_game()


if __name__ == '__main__':
    main()
