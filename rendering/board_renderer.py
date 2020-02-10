import pygame as pg

import colors
from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH
from rendering.window_renderer import MAIN_WINDOW


BOARD_LENGTH = 16
BOARD_HEIGHT = 10

def render_game_board(board_template):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            pg.draw.rect(MAIN_WINDOW, TILE_COLORS[board_template[y][x]],
                         (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT), 4)
