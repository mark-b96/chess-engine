import copy
from typing import List


class AI:
    def __init__(self):
        self.search_tree = None

    def get_optimal_move(self, board) -> List:
        board_value = board.get_board_value()
        node = Node(
            board=board,
            value=board_value
        )
        self.search_tree = Tree(root=node)
        search_tree_depth = 3

        # for _ in range(search_tree_depth):
        self.build_search_tree(root_node=node)
        for child_node in node.children:
            self.build_search_tree(root_node=child_node)

        optimal_board = node.children[0].board
        src, dst = optimal_board.current_move
        src_square = board.get_square(
            row=src.row,
            column=src.column
        )
        dst_square = board.get_square(
            row=dst.row,
            column=dst.column
        )
        return [src_square, dst_square]

    @staticmethod
    def build_search_tree(root_node):
        root_board = root_node.board
        all_possible_moves = root_board.get_all_possible_moves()

        for move in all_possible_moves:
            src_square, moves = move

            for possible_move in moves:
                board = copy.deepcopy(root_board)
                move_src_square = board.get_square(
                    row=src_square.row,
                    column=src_square.column
                )
                move_dst_square = board.get_square(
                    row=possible_move.row,
                    column=possible_move.column
                )
                board.update_board(
                    src_square=move_src_square,
                    dst_square=move_dst_square,
                )

                board_value = board.get_board_value()
                node = Node(
                    board=board,
                    value=board_value
                )
                root_node.children.append(node)
                node.parent = root_node


class Tree:
    def __init__(self, root):
        self.root = root
        self.depth = 0

    def insert(self):
        pass


class Node:
    def __init__(self, board, value):
        self.board = board
        self.value = value
        self.parent = None
        self.children = []


