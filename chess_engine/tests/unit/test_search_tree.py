from chess_engine.ai import Node, AI
from chess_engine.board import Board
import chess


def test_add_layer_to_search_tree():
    board_obj = Board()
    # board_obj.fen_repr = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ"
    # board_obj.fen_repr = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w"
    # board_obj.fen_repr = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w"
    board_obj.fen_repr = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq"
    board_obj.initialise_board()
    ai_obj = AI()

    board_value = board_obj.get_board_value()
    node = Node(
        board=board_obj,
        value=board_value
    )

    updated_nodes = []
    nodes = [node]

    for depth in range(4):
        for node in nodes:
            updated_nodes.extend(ai_obj.add_layer_to_search_tree(root_node=node))
            child_board_obj = node.board
            fen_rep = child_board_obj.get_fen()
            board = chess.Board(fen_rep)
            legal_moves = list(board.legal_moves)
            legal_moves_list = [str(_) for _ in legal_moves]

            actual_possible_moves = child_board_obj.get_all_possible_moves()
            actual_possible_moves_list = child_board_obj.moves_to_str(moves=actual_possible_moves)
            if len(legal_moves_list) != len(actual_possible_moves_list):
                print('')
            # for legal_move in legal_moves_list:
            #     assert legal_move in actual_possible_moves_list, f"\n{board}"
            # for actual_move in actual_possible_moves_list:
            #     assert actual_move in legal_moves_list, f"\n{board}"

        print(f"Depth: {depth + 1}")
        print(f"Number of nodes: {len(updated_nodes)}")

        nodes = updated_nodes
        updated_nodes = []


