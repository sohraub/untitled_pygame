import pygame as pg

import colors
from config import TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, TILE_COLORS
from game_elements.element_config_values import BOARD_LENGTH, BOARD_HEIGHT
from rendering.window_renderer import MAIN_WINDOW

"""
Module that will handle all of the rendering logic for the game boards.
"""

def render_game_board(board_template):
    """Renders a game board based on the template passed in."""
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            pg.draw.rect(MAIN_WINDOW, TILE_COLORS[board_template[y][x]],
                         (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (TOP_LEFT_X - 4, TOP_LEFT_Y - 4, PLAY_LENGTH + 8, PLAY_HEIGHT + 8), 4)
