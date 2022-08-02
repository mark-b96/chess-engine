import pygame as pg
from pathlib import Path
from typing import Tuple, List

from .square import Square

SQUARE_COLOURS = {
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 140, 0),
    "green": (0, 255, 0),
}


class GUI:
    def __init__(self, board_size, square_size):
        self.board_size: int = board_size
        self.square_size: int = square_size
        self.screen_size: int = self.board_size * self.square_size

        self.game_board = pg.display.set_mode([self.screen_size, self.screen_size])
        self.clock = pg.time.Clock()

    def load_piece(self, square: Square):
        piece_str = square.piece.__repr__().lower()
        icon_path = Path("./assets", f"{piece_str}.svg")
        piece_icon = pg.image.load(icon_path).convert_alpha(self.game_board)
        new_colour = square.piece.colour_code
        piece_icon.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        piece_icon.fill(new_colour, None, pg.BLEND_RGBA_ADD)
        return piece_icon

    def draw_piece(self, piece_icon, square: Square) -> None:
        self.game_board.blit(
            source=piece_icon,
            dest=(square.column * self.square_size, square.row * self.square_size),
        )

    def draw_square(self, square: Square, colour_str: str = None) -> None:
        colour = SQUARE_COLOURS.get(colour_str)
        square_dimensions = [
            self.square_size * square.column,
            self.square_size * square.row,
            self.square_size,
            self.square_size,
        ]
        pg.draw.rect(
            surface=self.game_board,
            color=square.colour_code if colour is None else colour,
            rect=square_dimensions,
        )

    @staticmethod
    def update_display() -> None:
        pg.display.update()

    def possible_squares(self, possible_squares: List[Square]):
        for square in possible_squares:
            self.draw_square(square, colour_str="green")
            if square.piece:
                self.draw_piece(square.piece.icon_asset, square)

    def clear_selection(self, possible_squares: List[Square]):
        for square in possible_squares:
            self.draw_square(square)
            if square.piece:
                self.draw_piece(square.piece.icon_asset, square)

    def event_listener(self) -> Tuple[int, int]:
        fps = 60
        while 1:
            self.clock.tick(fps)
            ev = pg.event.get()
            for event in ev:
                if not event.type == pg.MOUSEBUTTONDOWN:
                    continue
                x, y = pg.mouse.get_pos()
                row = y // self.square_size
                column = x // self.square_size
                return row, column

    def draw_game_board(self, chessboard: List[List[Square]]) -> None:
        for row in chessboard:
            for square in row:
                self.draw_square(square)
                if not square.piece:
                    continue
                piece_icon = self.load_piece(square)
                self.draw_piece(piece_icon, square)
                square.piece.icon_asset = piece_icon
        self.update_display()

    def update_squares(
        self, src_square: Square, dst_square: Square, valid_squares: List[Square]
    ) -> None:
        if not dst_square.piece.icon_asset:
            piece_icon = self.load_piece(dst_square)
            dst_square.piece.icon_asset = piece_icon
        self.clear_selection(valid_squares)
        self.draw_square(src_square)
