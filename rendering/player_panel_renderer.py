import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from game_elements.element_config_values import INVENTORY_LIMIT, INVENTORY_ROW_LENGTH
from rendering.window_renderer import MAIN_WINDOW,FONT_10, FONT_15, FONT_20, FONT_30, FONT_TNR_15


PANEL_TOP_LEFT_X = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) * 0.5)
PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) * 0.5)

# Inventory measurements
INVENTORY_LENGTH = int(0.95 * SIDE_PANEL_LENGTH)
INVENTORY_TOP_LEFT_X = int((SIDE_PANEL_LENGTH - INVENTORY_LENGTH) * 0.5) + PANEL_TOP_LEFT_X
INVENTORY_TOP_LEFT_Y = int(SIDE_PANEL_HEIGHT * 0.45) + PANEL_TOP_LEFT_Y
INVENTORY_NUM_ROWS = int(INVENTORY_LIMIT / INVENTORY_ROW_LENGTH)
ITEM_SIZE = int(INVENTORY_LENGTH / INVENTORY_ROW_LENGTH)


def render_player_panel(player_dict):
    pg.draw.rect(MAIN_WINDOW, colors.WHITE,
                 (PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
    player_name = FONT_30.render(player_dict['name'], 1, colors.WHITE)
    MAIN_WINDOW.blit(player_name, (PANEL_TOP_LEFT_X + 5, PANEL_TOP_LEFT_Y + 5))
    draw_hp_mp(player_dict['hp'], player_dict['mp'])
    draw_conditions(player_dict['conditions'])
    draw_attributes(player_dict['attributes'])
    draw_level_and_experience(player_dict['level'], player_dict['type'], player_dict['experience'])

    return pg.Rect(PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT)


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

def draw_inventory(inventory, refresh=False):
    inventory_label = FONT_20.render("INVENTORY", 1, colors.WHITE)
    MAIN_WINDOW.blit(inventory_label, (INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y - 25))
    inventory_rect = pg.Rect(INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y,
                             ITEM_SIZE * int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS), ITEM_SIZE * INVENTORY_NUM_ROWS)
    if refresh:
        MAIN_WINDOW.fill(color=colors.BLACK, rect=inventory_rect)
    inventory_tiles = list()
    for y in range(INVENTORY_NUM_ROWS):
        for x in range(int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS)):
            item_tile = pg.Rect((x * ITEM_SIZE) + INVENTORY_TOP_LEFT_X,
                                (y * ITEM_SIZE) + INVENTORY_TOP_LEFT_Y, ITEM_SIZE, ITEM_SIZE)
            pg.draw.rect(MAIN_WINDOW, colors.GREY, item_tile, 1)
            if len(inventory) >= (y * 10) + x + 1:
                MAIN_WINDOW.fill(color=colors.ORANGE, rect=((x * ITEM_SIZE) + INVENTORY_TOP_LEFT_X + 1,
                                                            (y * ITEM_SIZE) + INVENTORY_TOP_LEFT_Y + 1,
                                                             ITEM_SIZE - 2, ITEM_SIZE - 2))
                inventory_tiles.append(item_tile)
    return inventory_tiles, inventory_rect

def draw_item_info(item_dict, mouse_pos):
    """
    Function to draw a small window displaying item info. The top-left of the window will be determined by the position
    of the item in the inventory, so that the window will be enclosed by the inventory rectangle while also allowing
    the item to be invisible. Thus we have the window to appear to the left of the cursor if the item is in the right
    half of the inventory, and to the right of the cursor if the item is in the left half. The location of the mouse
    cursor is used to determine this.
    """
    item_window_length = int(INVENTORY_LENGTH / 2)
    item_window_height = ITEM_SIZE * 2
    top_left_y = INVENTORY_TOP_LEFT_Y
    if mouse_pos[0] < PANEL_TOP_LEFT_X + int(SIDE_PANEL_LENGTH / 2):
        # Cursor is on the left side of the inventory
        top_left_x = mouse_pos[0]
    else:
        # Cursor is on the right side of the inventory
        top_left_x = mouse_pos[0] - item_window_length
    MAIN_WINDOW.fill(colors.NAVY, (top_left_x, top_left_y, item_window_length, item_window_height))
    item_name = FONT_20.render(item_dict['name'].upper(), 1, colors.WHITE)
    # ['description'] and ['details'] are both lists of strings which we concatenate to add in a single loop
    item_string_list = item_dict['description'] + ['---'] + item_dict['details']
    item_details = [FONT_TNR_15.render(string, 1, colors.WHITE) for string in item_string_list]
    MAIN_WINDOW.blit(item_name, (top_left_x + 2, top_left_y + 2))
    for i, detail in enumerate(item_details):
        MAIN_WINDOW.blit(detail, (top_left_x + 5, top_left_y + 27 + (i *16)))
    pg.display.update()


