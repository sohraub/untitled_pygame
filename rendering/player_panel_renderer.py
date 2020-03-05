import pygame as pg

import colors

from config import WINDOW_HEIGHT, TOP_LEFT_X, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from game_elements.element_config_values import INVENTORY_LIMIT, INVENTORY_ROW_LENGTH
from rendering.window_renderer import MAIN_WINDOW, FONT_20, FONT_30, FONT_TNR_13, draw_detail_window

"""
Module for rendering the player panel on the left side of the screen. All the drawing functions return the rectangle
that's enclosing their subject, to be passed back to the PlayerPanel object which uses them to detect and handle 
mouseovers.

The following are the dimensions for all the rectangle drawn in this panel.
"""

#### MAIN PANEL ####
PANEL_TOP_LEFT_X = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) * 0.5)
PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) * 0.5)

#### INVENTORY ####
INVENTORY_LENGTH = int(0.95 * SIDE_PANEL_LENGTH)
INVENTORY_TOP_LEFT_X = int((SIDE_PANEL_LENGTH - INVENTORY_LENGTH) * 0.5) + PANEL_TOP_LEFT_X
INVENTORY_TOP_LEFT_Y = int(SIDE_PANEL_HEIGHT * 0.45) + PANEL_TOP_LEFT_Y
INVENTORY_NUM_ROWS = int(INVENTORY_LIMIT / INVENTORY_ROW_LENGTH)
ITEM_LENGTH = int(INVENTORY_LENGTH / INVENTORY_ROW_LENGTH)  # Items are stored as square tiles.


def draw_player_panel(player_dict):
    """
    Renders the main window and player name.
    :param player_dict:
    :return: panel_rect, the rect that makes up the main panel
    """
    panel_rect = pg.Rect(PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE, panel_rect, 2)
    player_name = FONT_30.render(player_dict['name'], 1, colors.WHITE)
    MAIN_WINDOW.blit(player_name, (PANEL_TOP_LEFT_X + 5, PANEL_TOP_LEFT_Y + 5))

    return panel_rect


def draw_level_and_experience(level, type, experience, refresh=False):
    """
    Renders the players level, type, and experience bar.
    :param level: An int which is the player's current level.
    :param type: A string which is the player's current type/class.
    :param experience: A list which stores the players experience progress as [current, max].
    :param refresh: A boolean which determines if the area around this info is filled to black, as a refresh.
    :return: The Rect enclosing all of the level and experience info.
    """
    level_and_exp_rect = (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 220, SIDE_PANEL_LENGTH - 20, 35)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, level_and_exp_rect)
    level_indicator = FONT_20.render(f"LEVEL {level} {type.upper()}", 1, colors.WHITE)
    MAIN_WINDOW.blit(level_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 220))
    pg.draw.rect(MAIN_WINDOW, colors.GREY,
                 (PANEL_TOP_LEFT_X + 6, PANEL_TOP_LEFT_Y + 248, SIDE_PANEL_LENGTH - 12, 8), 1)
    exp_percent = experience[0] / experience[1]
    current_exp_length = int(exp_percent * (SIDE_PANEL_LENGTH - 18 - PANEL_TOP_LEFT_X))
    if current_exp_length > 0:
        pg.draw.rect(MAIN_WINDOW, colors.PALE_YELLOW,
                     (PANEL_TOP_LEFT_X + 7, PANEL_TOP_LEFT_Y + 249, current_exp_length, 6), 0)

    return level_and_exp_rect


def draw_attributes(attributes, refresh=False):
    """
    Renders the player's attributes.
    :param attributes: A dict containing all of the players attribute values.
    :param refresh: A boolean determining if the area around this info is filled to black, as a refresh.
    :return: The Rect object enclosing the attributes.
    """
    attributes_rect = (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 120, SIDE_PANEL_LENGTH - 20, 75)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, attributes_rect)
    coord_mapping = {
        'str': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 120),
        'dex': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 145),
        'int': (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 170),
        'end': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 120),
        'vit': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 145),
        'wis': (PANEL_TOP_LEFT_X + 120, PANEL_TOP_LEFT_Y + 170)
    }
    font = pg.font.Font(font_SIL, 20)
    for stat in coord_mapping:
        string = "{0}: {1}".format(stat.upper(), attributes[stat])
        stat_indicator = font.render(string, 1, colors.WHITE)
        MAIN_WINDOW.blit(stat_indicator, coord_mapping[stat])

    return attributes_rect

def draw_hp_mp(hp, mp, refresh=False):
    """
    Renders the player's HP and MP.
    :param hp: A list storing the player's current HP level as  [current, max]
    :param mp: A list storing the player's current MP level as  [current, max]
    :param refresh: As above.
    :return: The Rect object that encloses hp and mp.
    """
    hp_mp_rect = (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 40, PANEL_TOP_LEFT_X + 100, 50)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, hp_mp_rect)
    hp_indicator = FONT_20.render("HP: {0} / {1}".format(hp[0], hp[1]), 1, colors.RED)
    mp_indicator = FONT_20.render("MP: {0} / {1}".format(mp[0], mp[1]), 1, colors.BLUE)
    MAIN_WINDOW.blit(hp_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 40))
    MAIN_WINDOW.blit(mp_indicator, (PANEL_TOP_LEFT_X + 10, PANEL_TOP_LEFT_Y + 65))
    return hp_mp_rect


def draw_conditions(conditions, refresh=False):
    """
    Renders the player's current condition levels.
    :param conditions: A dict containing each condition and it's level as [current, max, counter]. Counter isn't
                       used in this module.
    :param refresh: As above.
    :return: The Rect object that encloses the conditions.
    """
    condition_rect = (PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - 90, PANEL_TOP_LEFT_Y + 10, 80, 90)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, condition_rect)
    condition_y_mapping = {'thirsty': 10, 'hungry': 35, 'tired': 60}
    for condition in conditions:
        # Condition names are only rendered if the level is below 50%
        if conditions[condition][0] < 0.5 * conditions[condition][1]:
            current = conditions[condition][0]
            max = conditions[condition][1]
            # Condition font color is:
            #   yellow if level is in [35%, 50%)
            #   orange if level is in [15%, 35%)
            #   red if level is in [0$%, 15)
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
    return pg.Rect(condition_rect)

def draw_inventory(inventory, refresh=False):
    """
    Draws the player inventory.
    :param inventory: A list of every Item object in the players inventory.
    :param refresh: As above.
    :return: inventory_tile, a list of every item rect in the inventory, and inventory_rect the rect of the whole
             inventory
    """
    inventory_label = FONT_20.render("INVENTORY", 1, colors.WHITE)
    MAIN_WINDOW.blit(inventory_label, (INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y - 25))
    inventory_rect = pg.Rect(INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y,
                             ITEM_LENGTH * int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS), ITEM_LENGTH * INVENTORY_NUM_ROWS)
    if refresh:
        MAIN_WINDOW.fill(color=colors.BLACK, rect=inventory_rect)
    inventory_tiles = list()
    for y in range(INVENTORY_NUM_ROWS):
        for x in range(int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS)):
            item_tile = pg.Rect((x * ITEM_LENGTH) + INVENTORY_TOP_LEFT_X,
                                (y * ITEM_LENGTH) + INVENTORY_TOP_LEFT_Y, ITEM_LENGTH, ITEM_LENGTH)
            pg.draw.rect(MAIN_WINDOW, colors.GREY, item_tile, 1)
            if len(inventory) >= (y * 10) + x + 1:
                MAIN_WINDOW.fill(color=colors.ORANGE, rect=((x * ITEM_LENGTH) + INVENTORY_TOP_LEFT_X + 1,
                                                            (y * ITEM_LENGTH) + INVENTORY_TOP_LEFT_Y + 1,
                                                            ITEM_LENGTH - 2, ITEM_LENGTH - 2))
                inventory_tiles.append(item_tile)
    return inventory_tiles, inventory_rect

def draw_item_info(item_dict):
    """
    Function to draw a small window displaying item info. The top-left of the window will be determined by the position
    of the item in the inventory, so that the window will be enclosed by the inventory rectangle while also allowing
    the item to be invisible. Thus we have the window to appear to the left of the cursor if the item is in the right
    half of the inventory, and to the right of the cursor if the item is in the left half. The location of the mouse
    cursor is used to determine this.
    """

    mouse_pos = pg.mouse.get_pos()
    item_window_length = int(INVENTORY_LENGTH / 2)
    item_window_height = ITEM_LENGTH * 2
    top_left_y = INVENTORY_TOP_LEFT_Y
    if mouse_pos[0] < PANEL_TOP_LEFT_X + int(SIDE_PANEL_LENGTH / 2):
        # Cursor is on the left side of the inventory
        top_left_x = mouse_pos[0]
    else:
        # Cursor is on the right side of the inventory
        top_left_x = mouse_pos[0] - item_window_length

    # Body strings will be constructed differently for consumables and equipment.
    if item_dict['type'] == 'consumable':
        body_strings = item_dict['description'] + ['---'] + item_dict['details']

    draw_detail_window(body_strings=body_strings,
                       rect_dimensions=(top_left_x, top_left_y, item_window_length, item_window_height),
                       header_string=item_dict['name'].upper())

def draw_condition_details(conditions_dict, conditions_rect):
    """
    Function to display details on the players conditions when they are moused over.
    :param conditions_dict: A dict containing the player's condition info
    :param conditions_rect: The Rect enclosing the condition info, for positioning purposes
    """
    adj_to_noun = {  # A dict to map the conditions to nouns for display in the item detail windows
        'thirsty': 'Thirst',
        'hungry': 'Hunger',
        'tired': 'Tiredness'
    }
    top_left_x = conditions_rect[0] - 150
    top_left_y = conditions_rect[1]
    width = 145
    height = conditions_rect[3] - 30
    window_body = list()
    for condition in conditions_dict:
        current = conditions_dict[condition][0]
        max = conditions_dict[condition][1]
        window_body.append(f'{adj_to_noun[condition]} level: {current} / {max}')

    draw_detail_window(body_strings=window_body, rect_dimensions=(top_left_x, top_left_y, width, height), font_size=15)
