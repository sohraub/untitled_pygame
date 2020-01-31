import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, SHADOWS_INTO_LIGHT


panel_top_left_x = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2)
panel_top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)


def draw_conditions(window, player):
    hp_string = "HP: {0} / {1}".format(player.condition['HP'][0], player.condition['HP'][1])
    mp_string = "MP: {0} / {1}".format(player.condition['MP'][0], player.condition['MP'][1])
    font = pg.font.Font(SHADOWS_INTO_LIGHT, 20)
    hp_indicator = font.render(hp_string, 1, colors.RED)
    mp_indicator = font.render(mp_string, 1, colors.BLUE)
    window.blit(hp_indicator, (panel_top_left_x + 10, panel_top_left_y + 40))
    window.blit(mp_indicator, (panel_top_left_x + 10, panel_top_left_y + 65))
    for item in ['tired', 'hungry', 'thirsty']:
        if player.condition[item][0] < 0.5 * player.condition[item][1]:
            display_condition_state(window, player, item)


def display_condition_state(window, player, condition):
    condition_y_mapping = {'thirsty': 10, 'hungry': 35, 'tired': 60}
    current = player.condition[condition][0]
    max = player.condition[condition][1]
    if current < 0.15 * max:
        color = colors.RED
    elif current < 0.35 * max:
        color = colors.ORANGE
    else:
        color = colors.YELLOW
    font = pg.font.Font(SHADOWS_INTO_LIGHT, 20)
    condition_indicator = font.render(condition.upper(), 1, color)
    window.blit(condition_indicator, (panel_top_left_x + SIDE_PANEL_LENGTH - 90,
                                      panel_top_left_y + condition_y_mapping[condition]))


def display_attributes(window, player):
    coord_mapping = {
        'str': (panel_top_left_x + 10, panel_top_left_y + 120),
        'dex': (panel_top_left_x + 10, panel_top_left_y + 145),
        'int': (panel_top_left_x + 10, panel_top_left_y + 170),
        'end': (panel_top_left_x + 120, panel_top_left_y + 120),
        'vit': (panel_top_left_x + 120, panel_top_left_y + 145),
        'wis': (panel_top_left_x + 120, panel_top_left_y + 170)
    }
    font = pg.font.Font(SHADOWS_INTO_LIGHT, 20)
    for stat in coord_mapping.keys():
        string = "{0}: {1}".format(stat.upper(), player.attributes[stat])
        stat_indicator = font.render(string, 1, colors.WHITE)
        window.blit(stat_indicator, coord_mapping[stat])


def draw_level_and_experience(window, player):
    font = pg.font.Font(SHADOWS_INTO_LIGHT, 20)
    level_indicator = font.render("LEVEL {} {}".format(player.level, player.type.upper()), 1, colors.WHITE)
    window.blit(level_indicator, (panel_top_left_x + 10, panel_top_left_y + 220))
    pg.draw.rect(window, colors.GREY,
                 (panel_top_left_x + 6, panel_top_left_y + 248, SIDE_PANEL_LENGTH - 12, 8), 1)
    exp_percent = player.experience[0] / player.experience[1]
    current_exp_length = int(exp_percent * (SIDE_PANEL_LENGTH - 18 - panel_top_left_x))
    if current_exp_length > 0:
        pg.draw.rect(window, colors.PALE_YELLOW,
                     (panel_top_left_x + 7, panel_top_left_y + 249, current_exp_length, 6), 0)

def draw_player_panel(window, player):
    pg.draw.rect(window, colors.WHITE,
                 (panel_top_left_x, panel_top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
    font = pg.font.Font(SHADOWS_INTO_LIGHT, 30)
    player_name = font.render(player.name, 1, colors.WHITE)
    window.blit(player_name, (panel_top_left_x + 5, panel_top_left_y + 5))
    draw_conditions(window, player)
    display_attributes(window, player)
    draw_level_and_experience(window, player)



