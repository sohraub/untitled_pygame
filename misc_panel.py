import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, SHADOWS_INTO_LIGHT


panel_top_left_x = WINDOW_LENGTH - ((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2) - SIDE_PANEL_LENGTH
panel_top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)


def draw_misc_panel(window, board, focus_tile=None):
    pg.draw.rect(window, colors.WHITE, (panel_top_left_x, panel_top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
    draw_focus_window(window, board, focus_tile)


def draw_focus_window(window, board, focus_tile=None):
    top_left_x = panel_top_left_x + int(0.02*SIDE_PANEL_LENGTH)
    top_left_y = panel_top_left_y + int(0.02*SIDE_PANEL_HEIGHT)
    length = int(0.96*SIDE_PANEL_LENGTH)
    height = int(0.3*SIDE_PANEL_HEIGHT)
    pg.draw.rect(window, colors.WHITE, (top_left_x, top_left_y, length, height), 1)
    if focus_tile is not None:
        # This mapping gives the appropriate function to load data, based on the type of tile which under focus
        focus_function_mapping = {
            'E': load_enemy_info
        }
        tile_type = board.template[focus_tile[1]][focus_tile[0]]  # Get the tile letter from the board template
        focus_function_mapping[tile_type](top_left_x, top_left_y, length, height, window, board, focus_tile)


def load_enemy_info(top_left_x, top_left_y, f_window_length, f_window_height, window, board, focus_tile):
    enemy = board.enemies[focus_tile]
    portrait_top_left_x = top_left_x + int(0.025*f_window_length)
    portrait_top_left_y = top_left_y + int(0.025*f_window_height)
    portrait_length = int(0.19*f_window_length)
    portrait_height = int(0.3*f_window_height)
    pg.draw.rect(window, colors.WHITE, (portrait_top_left_x, portrait_top_left_y, portrait_length, portrait_height), 1)
    big_font = pg.font.Font(SHADOWS_INTO_LIGHT, 30)
    small_font = pg.font.Font(SHADOWS_INTO_LIGHT, 15)
    enemy_name = big_font.render(' '.join(enemy.name.split('_')[0:-1]).upper(), 1, colors.WHITE)
    window.blit(enemy_name, (portrait_top_left_x + portrait_length + 5, portrait_top_left_y))
