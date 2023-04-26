from typing import List

from chess_engine.backend.board import Board

SEARCH_DEPTH = 3


class Node:
    def __init__(self, board, value=0, move=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = None
        self.children = []


class AI:
    def get_optimal_move(self, board: Board) -> List:
        node = Node(board=board)

        best_value, best_node = self.alpha_beta(
            node=node,
            depth=SEARCH_DEPTH,
            alpha=-99999,
            beta=99999,
            is_maximising_player=True
        )
        while best_node.parent.parent:
            best_node = best_node.parent
        best_move = best_node.move
        src, dst = best_move
        src_square = board.get_square(row=src.row, column=src.column)
        dst_square = board.get_square(row=dst.row, column=dst.column)
        return [src_square, dst_square, board.promotion_piece]

    @staticmethod
    def add_layer_to_search_tree(root_node: Node, is_maximising_player: bool):
        root_board = root_node.board
        root_fen_repr = root_board.get_fen()
        all_possible_moves = root_board.get_all_possible_moves()

        for move in all_possible_moves:
            src_square, moves = move

            for possible_move in moves:
                board = Board()
                board.fen_repr = root_fen_repr
                board.initialise_board()
                if isinstance(possible_move, List):
                    board.promotion_piece = possible_move[1]
                    possible_move = possible_move[0]
                move_src_square = board.get_square(
                    row=src_square.row, column=src_square.column
                )
                move_dst_square = board.get_square(
                    row=possible_move.row, column=possible_move.column
                )
                board.update_board(
                    src_square=move_src_square,
                    dst_square=move_dst_square,
                )

                board_value = board.get_board_value(is_maximising_player=is_maximising_player)
                node = Node(board=board, value=board_value, move=[move_src_square, move_dst_square])
                node.board.is_whites_turn = not node.board.is_whites_turn
                root_node.children.append(node)
                node.parent = root_node
                del board
        return root_node.children

    def alpha_beta(
            self, node: Node, depth: int, alpha: int, beta: int, is_maximising_player: bool
    ) -> [int, Node]:
        if depth == 0 or node.board.is_terminal:
            return node.value, node

        child_node_list = self.add_layer_to_search_tree(root_node=node, is_maximising_player=is_maximising_player)

        if is_maximising_player:
            best_value = -99999
            best_node = None
            for child_node in child_node_list:
                value, calc_node = self.alpha_beta(
                    node=child_node,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_maximising_player=False
                )
                if value > best_value:
                    best_value = value
                    best_node = calc_node

                if value > beta:
                    break
                alpha = max(alpha, value)

            return best_value, best_node

        else:
            best_value = 99999
            best_node = None
            for child_node in child_node_list:
                value, calc_node = self.alpha_beta(
                    node=child_node,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_maximising_player=True
                )
                if value < best_value:
                    best_value = value
                    best_node = calc_node

                if value < alpha:
                    break
                beta = min(beta, value)

            return best_value, best_node

