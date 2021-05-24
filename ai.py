import random


class AI(object):
    def __init__(self):
        pass

    def move(self, white_move, board):
        if white_move:
            pieces = board.white_pieces.copy()
        else:
            pieces = board.black_pieces.copy()
        all_possible_moves = []
        for square in pieces:
            possible_moves = board.get_piece_moves(square)
            if possible_moves:
                all_possible_moves.append([square, possible_moves])
        last_index = len(all_possible_moves) - 1
        move_index = random.randint(0, last_index)
        piece, moves = all_possible_moves[move_index]
        final_move = [piece, random.choice(moves)]
        return final_move
