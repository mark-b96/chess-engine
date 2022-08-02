from typing import List
from chess_engine.board import Board


class AI:
    def __init__(self):
        self.search_tree = None

    def get_optimal_move(self, board) -> List:
        board_value = board.get_board_value()
        node = Node(board=board, value=board_value)
        self.search_tree = Tree(root=node)
        search_tree_depth = 5
        nodes = [node]
        updated_nodes = []

        for depth in range(search_tree_depth):
            for node in nodes:
                updated_nodes.extend(self.add_layer_to_search_tree(root_node=node))

            updated_nodes = []
        move = board.all_possible_moves[0]
        src, dst = move
        dst = dst[0]
        src_square = board.get_square(row=src.row, column=src.column)
        dst_square = board.get_square(row=dst.row, column=dst.column)
        return [src_square, dst_square, board.promotion_piece]

    def add_layer_to_search_tree(self, root_node):
        root_board = root_node.board
        all_possible_moves = root_board.get_all_possible_moves()

        for move in all_possible_moves:
            src_square, moves = move

            for possible_move in moves:
                board = Board()
                fen_repr = root_board.get_fen()
                board.fen_repr = fen_repr
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

                board_value = board.get_board_value()
                node = Node(board=board, value=board_value)
                node.board.is_whites_turn = not node.board.is_whites_turn
                self.search_tree.total_nodes += 1
                root_node.children.append(node)
                node.parent = root_node
                del board
        return root_node.children


class Tree:
    def __init__(self, root):
        self.root = root
        self.depth = 0
        self.total_nodes = 0

    def insert(self):
        pass


class Node:
    def __init__(self, board, value):
        self.board = board
        self.value = value
        self.parent = None
        self.children = []
