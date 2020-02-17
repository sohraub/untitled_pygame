import pygame as pg

import colors
from config import TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, TILE_COLORS, BOARD_HEIGHT, BOARD_LENGTH
from rendering.window_renderer import MAIN_WINDOW



def render_game_board(board_template):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            pg.draw.rect(MAIN_WINDOW, TILE_COLORS[board_template[y][x]],
                         (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (TOP_LEFT_X - 4, TOP_LEFT_Y - 4, PLAY_LENGTH + 8, PLAY_HEIGHT + 8), 4)
