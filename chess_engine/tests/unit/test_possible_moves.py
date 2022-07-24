import chess
from chess_engine.board import Board


def test_possible_moves():
    board = chess.Board("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ")
    legal_moves = list(board.legal_moves)
    legal_moves_list = [str(_) for _ in legal_moves]

    board_obj = Board()
    parsed_fen_list = board_obj.parse_fen(fen_str="rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ")
    board_obj.initialise_board(
        parsed_fen_list=parsed_fen_list,
    )
    actual_possible_moves = board_obj.get_all_possible_moves()
    actual_possible_moves_list = board_obj.moves_to_str(moves=actual_possible_moves)
    for move in legal_moves_list:
        assert move in actual_possible_moves_list
