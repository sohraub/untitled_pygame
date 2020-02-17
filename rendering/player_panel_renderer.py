import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from rendering.window_renderer import MAIN_WINDOW, FONT_20, FONT_30


PANEL_TOP_LEFT_X = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2)
PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)


def render_player_panel(player_dict):
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
    player_name = FONT_30.render(player_dict['name'], 1, colors.WHITE)
    MAIN_WINDOW.blit(player_name, (PANEL_TOP_LEFT_X + 5, PANEL_TOP_LEFT_Y + 5))
    draw_hp_mp(player_dict['hp'], player_dict['mp'])
    draw_conditions(player_dict['conditions'])
    draw_attributes(player_dict['attributes'])
    draw_level_and_experience(player_dict['level'], player_dict['type'], player_dict['experience'])


def draw_level_and_experience(level, type, experience, refresh=False):
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 220, SIDE_PANEL_LENGTH - 20, 35))
    level_indicator = FONT_20.render("LEVEL {} {}".format(level, type.upper()), 1, colors.WHITE)
    MAIN_WINDOW.blit(level_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 220))
    pg.draw.rect(MAIN_WINDOW, colors.GREY,
                 (PANEL_TOP_LEFT_X + 6, PANEL_TOP_LEFT_Y + 248, SIDE_PANEL_LENGTH - 12, 8), 1)
    exp_percent = experience[0] / experience[1]
    current_exp_length = int(exp_percent * (SIDE_PANEL_LENGTH - 18 - PANEL_TOP_LEFT_X))
    if current_exp_length > 0:
        pg.draw.rect(MAIN_WINDOW, colors.PALE_YELLOW,
                     (PANEL_TOP_LEFT_X + 7, PANEL_TOP_LEFT_Y + 249, current_exp_length, 6), 0)


def draw_attributes(attributes, refresh=False):
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 120, SIDE_PANEL_LENGTH - 20, 75))
    coord_mapping = {
        'str': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 120),
        'dex': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 145),
        'int': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 170),
        'end': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 120),
        'vit': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 145),
        'wis': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 170)
    }
    font = pg.font.Font(font_SIL, 20)
    for stat in coord_mapping.keys():
        string = "{0}: {1}".format(stat.upper(), attributes[stat])
        stat_indicator = font.render(string, 1, colors.WHITE)
        MAIN_WINDOW.blit(stat_indicator, coord_mapping[stat])


def draw_hp_mp(hp, mp, refresh=False):
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 40, PANEL_TOP_LEFT_X + 100, 50))
    hp_indicator = FONT_20.render("HP: {0} / {1}".format(hp[0], hp[1]), 1, colors.RED)
    mp_indicator = FONT_20.render("MP: {0} / {1}".format(mp[0], mp[1]), 1, colors.BLUE)
    MAIN_WINDOW.blit(hp_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 40))
    MAIN_WINDOW.blit(mp_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 65))


def draw_conditions(conditions, refresh=False):
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, (PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - 90, PANEL_TOP_LEFT_Y + 10, 80, 90))
    condition_y_mapping = {'thirsty': 10, 'hungry': 35, 'tired': 60}
    for condition in conditions:
        if conditions[condition][0] < 0.5 * conditions[condition][1]:
            current = conditions[condition][0]
            max = conditions[condition][1]
            if current < 0.15 * max:
                color = colors.RED
            elif current < 0.35 * max:
                color = colors.ORANGE
            else:
                color = colors.YELLOW
            font = pg.font.Font(font_SIL, 20)
            condition_indicator = font.render(condition.upper(), 1, color)
            MAIN_WINDOW.blit(condition_indicator, (PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - 90,
                                                   PANEL_TOP_LEFT_Y + condition_y_mapping[condition]))
