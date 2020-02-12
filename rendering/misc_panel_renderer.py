import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from rendering.window_renderer import MAIN_WINDOW, FONT_15, FONT_20, FONT_30


PANEL_TOP_LEFT_X = WINDOW_LENGTH - ((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2) - SIDE_PANEL_LENGTH
PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)

F_WINDOW_TOP_LEFT_X = PANEL_TOP_LEFT_X + int(0.02 * SIDE_PANEL_LENGTH)  # Top-left coords for the focus window
F_WINDOW_TOP_LEFT_Y = PANEL_TOP_LEFT_Y + int(0.02 * SIDE_PANEL_HEIGHT)
F_WINDOW_LENGTH = int(0.96 * SIDE_PANEL_LENGTH)
F_WINDOW_HEIGHT = int(0.3 * SIDE_PANEL_HEIGHT)

PORTRAIT_TOP_LEFT_X = F_WINDOW_TOP_LEFT_X + int(0.025 * F_WINDOW_LENGTH)
PORTRAIT_TOP_LEFT_Y = F_WINDOW_TOP_LEFT_Y + int(0.025 * F_WINDOW_HEIGHT)
PORTRAIT_LENGTH = int(0.19 * F_WINDOW_LENGTH)
PORTRAIT_HEIGHT = int(0.3 * F_WINDOW_HEIGHT)


def render_misc_panel():
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)

def render_focus_window(focus_info=None):
    f_window_rect = (F_WINDOW_TOP_LEFT_X, F_WINDOW_TOP_LEFT_Y, F_WINDOW_LENGTH, F_WINDOW_HEIGHT)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE, f_window_rect, 1)
    if focus_info is not None:
        # Re-fill the area just inside the window to black, as a refresh
        MAIN_WINDOW.fill(colors.BLACK,
                         rect=(f_window_rect[0]+1, f_window_rect[1]+1, f_window_rect[2]-2, f_window_rect[3]-2))
        if focus_info['type'] == 'enemy':
            render_enemy_info(focus_info)

def render_enemy_info(enemy_dict):
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y, PORTRAIT_LENGTH, PORTRAIT_HEIGHT), 1)

    enemy_hp_percentage = float(enemy_dict['hp'][0]) / float(enemy_dict['hp'][1])
    if enemy_hp_percentage > 0.66:
        # TODO: These might need some work
        health_text = 'This creature looks quite healthy.'
    elif enemy_hp_percentage > 0.33:
        health_text = 'This creature seems to be in pain.'
    else:
        health_text = 'This creature is on the brink of death.'

    enemy_name = FONT_30.render(' '.join(enemy_dict['name'].split('_')[0:-1]).upper(), 1, colors.WHITE)
    flavour_text = FONT_15.render(enemy_dict['flavour_text'], 1, colors.WHITE)
    health_indicator = FONT_15.render(health_text, 1, colors.WHITE)

    MAIN_WINDOW.blit(enemy_name, (PORTRAIT_TOP_LEFT_X + PORTRAIT_LENGTH + 5, PORTRAIT_TOP_LEFT_Y))
    MAIN_WINDOW.blit(flavour_text, (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y + PORTRAIT_HEIGHT + 3))
    MAIN_WINDOW.blit(health_indicator, (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y + PORTRAIT_HEIGHT + 45))

