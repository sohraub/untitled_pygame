import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_X, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH
from rendering.window_renderer import MAIN_WINDOW, FONT_15, FONT_20, FONT_30

"""
Module which handles all of the rendering for the miscellaneous panel on the right side of the window.

The following are the dimension variables for all the different windows that are rendered in this panel.
"""

#### MAIN PANEL ####
PANEL_TOP_LEFT_X = WINDOW_LENGTH - ((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2) - SIDE_PANEL_LENGTH
PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)

#### FOCUS WINDOW ####
F_WINDOW_TOP_LEFT_X = PANEL_TOP_LEFT_X + int(0.02 * SIDE_PANEL_LENGTH)
F_WINDOW_TOP_LEFT_Y = PANEL_TOP_LEFT_Y + int(0.02 * SIDE_PANEL_HEIGHT)
F_WINDOW_LENGTH = int(0.96 * SIDE_PANEL_LENGTH)
F_WINDOW_HEIGHT = int(0.3 * SIDE_PANEL_HEIGHT)

#### ENEMY PORTRAITS ####
PORTRAIT_TOP_LEFT_X = F_WINDOW_TOP_LEFT_X + int(0.025 * F_WINDOW_LENGTH)
PORTRAIT_TOP_LEFT_Y = F_WINDOW_TOP_LEFT_Y + int(0.025 * F_WINDOW_HEIGHT)
PORTRAIT_LENGTH = int(0.19 * F_WINDOW_LENGTH)
PORTRAIT_HEIGHT = int(0.3 * F_WINDOW_HEIGHT)


def render_misc_panel():
    """Draws the main panel rectangle."""
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
    render_focus_window()

def render_focus_window(focus_info=None, refresh=False):
    """
    Draws the outer frame of the focus window, and fills it based on the focus tile, if it's not None.

    :param focus_info: A dict with a 'type' key that determines that specific function to draw the info, as well as all
                       the info needed by that function.
    :param refresh: Flag that determines whether or not the window is re-filled with black, as a refresh.
    :return: n/a
    """
    f_window_rect = (F_WINDOW_TOP_LEFT_X, F_WINDOW_TOP_LEFT_Y, F_WINDOW_LENGTH, F_WINDOW_HEIGHT)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE, f_window_rect, 1)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK,
                         rect=(f_window_rect[0] + 1, f_window_rect[1] + 1, f_window_rect[2] - 2, f_window_rect[3] - 2))
    if focus_info is not None:
        if focus_info['type'] == 'enemy':
            render_enemy_info(focus_info)

def render_enemy_info(enemy_dict):
    """
    Function for filling in all the focus window info when focusing an enemy.
    :param enemy_dict: A dict with all of the enemy details needed to display.
    :return: n/a
    """
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y, PORTRAIT_LENGTH, PORTRAIT_HEIGHT), 1)

    enemy_hp_percentage = float(enemy_dict['hp'][0]) / float(enemy_dict['hp'][1])
    # A bit of text will be added to the enemy description to indicate their health level.
    # TODO: These might need some work
    if enemy_hp_percentage > 0.66:
        health_text = 'This creature looks quite healthy.'
    elif enemy_hp_percentage > 0.33:
        health_text = 'This creature seems to be in pain.'
    else:
        health_text = 'This creature is on the brink of death.'

    # Enemy names are stored as {enemy type}_{uuid}, with underscores in the enemy names to separate words
    enemy_name = FONT_30.render(' '.join(enemy_dict['name'].split('_')[0:-1]).upper(), 1, colors.WHITE)
    flavour_text = FONT_15.render(enemy_dict['flavour_text'], 1, colors.WHITE)
    health_indicator = FONT_15.render(health_text, 1, colors.WHITE)

    MAIN_WINDOW.blit(enemy_name, (PORTRAIT_TOP_LEFT_X + PORTRAIT_LENGTH + 5, PORTRAIT_TOP_LEFT_Y))
    MAIN_WINDOW.blit(flavour_text, (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y + PORTRAIT_HEIGHT + 3))
    MAIN_WINDOW.blit(health_indicator, (PORTRAIT_TOP_LEFT_X, PORTRAIT_TOP_LEFT_Y + PORTRAIT_HEIGHT + 45))

