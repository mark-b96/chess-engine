import os
import pygame as pg


class GUI(object):
    def __init__(self, _width: int, _height: int):
        self.screen_width, self.screen_height = _width, _height
        self.game_board = pg.display.set_mode([self.screen_width, self.screen_height])
        self.square_size = self.screen_width//8
        self.clock = pg.time.Clock()

    def load_piece(self, square):
        piece_str = square.piece.__repr__().lower()
        icon_path = os.path.join('assets', '{}.svg'.format(piece_str))
        piece_icon = pg.image.load(icon_path).convert_alpha(self.game_board)
        new_colour = square.piece.colour_code
        piece_icon.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        piece_icon.fill(new_colour, None, pg.BLEND_RGBA_ADD)
        return piece_icon

    def draw_piece(self, piece_icon, square):
        self.game_board.blit(
            source=piece_icon,
            dest=(square.column * self.square_size, square.row * self.square_size)
        )

    def draw_square(self, square, colour=None):
        square_dimensions = [
            self.square_size * square.column,
            self.square_size * square.row,
            self.square_size,
            self.square_size
        ]
        pg.draw.rect(
            surface=self.game_board,
            color=square.colour_code if colour is None else colour,
            rect=square_dimensions
        )

    @staticmethod
    def update_display():
        pg.display.update()

    def possible_squares(self, possible_squares: list):
        colour = (0, 255, 0)
        for square in possible_squares:
            self.draw_square(square, colour=colour)
            if square.piece:
                self.draw_piece(square.piece.icon_asset, square)

    def clear_selection(self, possible_squares: list):
        for square in possible_squares:
            self.draw_square(square)
            if square.piece:
                self.draw_piece(square.piece.icon_asset, square)

    def event_listener(self) -> (int, int):
        fps = 60
        while 1:
            self.clock.tick(fps)
            ev = pg.event.get()
            for event in ev:
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    row = y // self.square_size
                    column = x // self.square_size
                    return row, column



