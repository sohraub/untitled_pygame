import pygame as pg
from copy import copy
from time import sleep

import colors
from config import TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, TILE_COLORS
from game_elements.element_config_values import BOARD_LENGTH, BOARD_HEIGHT
from rendering.window_renderer import MAIN_WINDOW
from utility_functions import find_tiles_in_radius, tile_from_xy_coords

"""
Module that will handle all of the rendering logic for the game boards.
"""

def render_game_board(board_template, tiles_to_highlight=None, highlight_color=colors.RED,
                      targetable_tile_types=None):
    """
    Renders a game board based on the template passed in. If tiles_to_highlight is not None, this implies that this
    function is being called to target certain tiles, usually in the case of a Player using an item or ability. In this
    case, we highlight the passed-in tiles with highlight_color, but only if they are in targetable_tile_types.
    """
    tiles_to_highlight = tiles_to_highlight if tiles_to_highlight is not None else set()
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            if (x, y) in tiles_to_highlight and board_template[y][x] in targetable_tile_types:
                pg.draw.rect(MAIN_WINDOW, highlight_color,
                             (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                continue
            pg.draw.rect(MAIN_WINDOW, TILE_COLORS[board_template[y][x]],
                         (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (TOP_LEFT_X - 4, TOP_LEFT_Y - 4, PLAY_LENGTH + 8, PLAY_HEIGHT + 8), 4)
    pg.display.update((TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT))


def highlight_adjacent_tiles(board_template, target_x, target_y, color=colors.BLACK):
    """
    Renders the game board with tiles adjacent to (target_x, target_y) highlighted. Obtains target tiles in pixel-
    coordinate format, to be used by for collision detection when the player selects a target with the mouse.
    """
    tiles_to_highlight = list()
    for i in [-1, 1]:
        tiles_to_highlight.append((target_x + i, target_y))
        tiles_to_highlight.append((target_x, target_y + i))

    render_game_board(board_template, tiles_to_highlight=set(tiles_to_highlight), highlight_color=color,
                      targetable_tile_types={'O', 'E', 'R'})
    return tiles_to_highlight


def highlight_self(board_template, target_x, target_y, color=colors.BLACK):
    """ Renders the game board with just the player highlighted. """
    render_game_board(board_template, tiles_to_highlight={(target_x, target_y)}, highlight_color=color,
                      targetable_tile_types={'P'})
    return [(target_x, target_y)]


def highlight_radius_with_splash_target(board_template, target_x, target_y, radius, *args, color=colors.BLACK):
    """
    Targets every open/trap tile on the board, and returns as a list of targets every tile directly adjacent to the
    tile selected.
    """
    potential_tiles_to_highlight = find_tiles_in_radius(center_x=target_x, center_y=target_y, radius=radius)
    print(target_x)
    print(target_y)
    print(radius)
    tiles_to_highlight = [(x, y) for (x, y) in potential_tiles_to_highlight if board_template[y][x] in {'O', 'R'}]
    render_game_board(board_template, tiles_to_highlight=set(tiles_to_highlight), highlight_color=color,
                      targetable_tile_types={'O', 'R'})
    return tiles_to_highlight


def animate_enemy_death(enemy_x, enemy_y):
    """
    Function to gradually change the color of an enemy, on death, so as to create the effect of fading to the
    background grey color, currently set to (173, 173, 173). On input of the enemy's coordinates, it works as follows:
        i. use the tile_from_xy_coords() function to get the dimensions and location of the enemy's Rect on the board
        ii. starting from the base red color for enemies, iteratively set the value of each hue to the average of
            the current value and 173. This will eventually converge to ~ 173.
        iii. The condition on the while loop can be read as:
                iterate until the sum of the 3 hue values lies between 3*170 and 3*175.
             This is done so that the animation doesn't end prematurely when one of the hues reaches ~173 before the
             other two, and to allow the loop to iterate fewer times as the visual difference of values from
             170-175 is largely negligible.
    """
    new_color = copy(TILE_COLORS['E'])
    enemy_rect = pg.Rect(tile_from_xy_coords(x=enemy_x, y=enemy_y))

    while not 510 < new_color[0] + new_color[1] + new_color[2] < 525:
        new_color = (int((new_color[0] + 173) / 2),
                     int((new_color[1] + 173) / 2),
                     int((new_color[2] + 173) / 2))
        MAIN_WINDOW.fill(rect=enemy_rect, color=new_color)
        pg.display.update(enemy_rect)
        sleep(0.1)
