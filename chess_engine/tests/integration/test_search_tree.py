import pytest
import chess

from chess_engine.ai import Node, AI
from chess_engine.board import Board


@pytest.mark.parametrize(
    "board_rep, expected_node_count",
    [
        ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", 63_909),
        ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", 9737),
        ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - - -", 3017),
        ("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10", 92_015),
        ("r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1", 9737),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 9322),
    ],
)
def test_possible_game_states(board_rep: str, expected_node_count: int):
    """
    Node counts obtained from: https://www.chessprogramming.org/Perft_Results#cite_note-7
    :param board_rep: FEN board representation
    :param expected_node_count: Number of game states
    """
    board_obj = Board()
    board_obj.fen_repr = board_rep
    board_obj.initialise_board()
    ai_obj = AI()

    board_value = board_obj.get_board_value()
    node = Node(board=board_obj, value=board_value)

    updated_nodes = []
    nodes = [node]

    total_nodes = 0

    for depth in range(3):
        for node in nodes:
            updated_nodes.extend(ai_obj.add_layer_to_search_tree(root_node=node))

        total_nodes += len(updated_nodes)

        nodes = updated_nodes
        updated_nodes = []

    assert total_nodes == expected_node_count


@pytest.mark.parametrize(
    "board_rep",
    [
        "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
        "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
        "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - - -",
        "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
        "r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    ],
)
def test_game_state_with_chess_package(board_rep: str):
    """
    :param board_rep: FEN board representation
    """
    board_obj = Board()
    board_obj.fen_repr = board_rep
    board_obj.initialise_board()
    ai_obj = AI()

    board_value = board_obj.get_board_value()
    node = Node(board=board_obj, value=board_value)

    updated_nodes = []
    nodes = [node]

    for depth in range(3):
        for node in nodes:
            updated_nodes.extend(ai_obj.add_layer_to_search_tree(root_node=node))
            child_board_obj = node.board
            fen_rep = child_board_obj.get_fen()
            board = chess.Board(fen_rep)
            legal_moves = list(board.legal_moves)
            legal_moves_list = [str(_) for _ in legal_moves]

            actual_possible_moves = child_board_obj.get_all_possible_moves()
            actual_possible_moves_list = child_board_obj.moves_to_str(
                moves=actual_possible_moves
            )
            for legal_move in legal_moves_list:
                assert legal_move in actual_possible_moves_list, f"\n{board}"
            for actual_move in actual_possible_moves_list:
                assert actual_move in legal_moves_list, f"\n{board}"

        nodes = updated_nodes
        updated_nodes = []
