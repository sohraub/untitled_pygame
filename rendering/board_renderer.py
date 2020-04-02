import pygame as pg

import colors
from config import TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, TILE_COLORS
from game_elements.element_config_values import BOARD_LENGTH, BOARD_HEIGHT
from rendering.window_renderer import MAIN_WINDOW

"""
Module that will handle all of the rendering logic for the game boards.
"""

def render_game_board(board_template, tiles_to_highlight=None, highlight_color=colors.RED):
    """
    Renders a game board based on the template passed in. If tiles_to_highlight is not None, this implies that this
    function is being called to target certain tiles, usually in the case of a Player using an item or ability. In this
    case, we highlight the passed-in tiles with highlight_color.
    """
    tiles_to_highlight = tiles_to_highlight if tiles_to_highlight is not None else set()
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            if (x, y) in tiles_to_highlight and board_template[y][x] in {'O', 'E', 'R'}:
                pg.draw.rect(MAIN_WINDOW, highlight_color,
                             (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                continue
            pg.draw.rect(MAIN_WINDOW, TILE_COLORS[board_template[y][x]],
                         (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (TOP_LEFT_X - 4, TOP_LEFT_Y - 4, PLAY_LENGTH + 8, PLAY_HEIGHT + 8), 4)


def highlight_adjacent_tiles(board_template, target_x, target_y, color=colors.RED):
    """
    Renders the game board with tiles adjacent to (target_x, target_y) highlighted. Obtains target tiles in pixel-
    coordinate format, to be used by for collision detection when the player selects a target with the mouse.
    """
    tiles_to_highlight = list()
    for i in [-1, 1]:
        tiles_to_highlight.append((target_x + i, target_y))
        tiles_to_highlight.append((target_x, target_y + i))

    render_game_board(board_template, tiles_to_highlight=set(tiles_to_highlight), highlight_color=color)
    pg.display.update()
    return tiles_to_highlight

