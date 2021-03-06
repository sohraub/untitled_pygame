import pygame as pg

import colors

from config import SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, PLAYER_PANEL_TOP_LEFT_X, PLAYER_PANEL_TOP_LEFT_Y, font_SIL
from game_elements.element_config_values import INVENTORY_LIMIT, INVENTORY_ROW_LENGTH
from rendering.window_renderer import MAIN_WINDOW, FONT_15, FONT_20, FONT_30, FONT_CALIBRI_12, draw_detail_window
from utility_functions import parse_description

"""
Module for rendering the player panel on the left side of the screen. All the drawing functions return the rectangle
that's enclosing their subject, to be passed back to the PlayerPanel object which uses them to detect and handle 
mouseovers.

The following are the dimensions for all the main rectangles drawn in this panel.
"""

#### INVENTORY ####
INVENTORY_LENGTH = int(0.95 * SIDE_PANEL_LENGTH)
INVENTORY_TOP_LEFT_X = int((SIDE_PANEL_LENGTH - INVENTORY_LENGTH) * 0.5) + PLAYER_PANEL_TOP_LEFT_X
INVENTORY_TOP_LEFT_Y = int(SIDE_PANEL_HEIGHT * 0.45) + PLAYER_PANEL_TOP_LEFT_Y
INVENTORY_NUM_ROWS = int(INVENTORY_LIMIT / INVENTORY_ROW_LENGTH)
ITEM_LENGTH = int(INVENTORY_LENGTH / INVENTORY_ROW_LENGTH)  # Items are stored as square tiles, so length = height

#### ITEM TOOLTIPS ####
ITEM_TOOLTIP_LENGTH = int(INVENTORY_LENGTH / 2)
ITEM_TOOLTIP_HEIGHT = ITEM_LENGTH * 2

#### EQUIPMENT ####
EQUIP_ITEM_LENGTH = int(ITEM_LENGTH * 0.75)  # Item tiles in equipment be 3/4ths the size of items in inventory.
EQUIPMENT_LENGTH = 3.8 * EQUIP_ITEM_LENGTH  # Equipment will be 3 items across and 3 items high, so set length, height to
EQUIPMENT_HEIGHT = 3.8 * EQUIP_ITEM_LENGTH  # be 4 * EQUIP_ITEM_LENGTH for a bit of extra wiggle-room.
EQUIPMENT_TOP_LEFT_X = PLAYER_PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - EQUIPMENT_LENGTH
EQUIPMENT_TOP_LEFT_Y = PLAYER_PANEL_TOP_LEFT_Y + int(0.175*SIDE_PANEL_HEIGHT)

#### ABILITIES ####
ABILITY_TILE_LENGTH = int(1.2 * ITEM_LENGTH)
ABILITIES_TOP_LEFT_X = INVENTORY_TOP_LEFT_X
ABILITIES_TOP_LEFT_Y = PLAYER_PANEL_TOP_LEFT_Y + int(0.7 * SIDE_PANEL_HEIGHT)

#### LEVEL/EXP INFO ####
LEVEL_EXP_TOP_LEFT_X = int(PLAYER_PANEL_TOP_LEFT_X * 1.25)
LEVEL_EXP_TOP_LEFT_Y = PLAYER_PANEL_TOP_LEFT_Y + int(0.9 * SIDE_PANEL_HEIGHT)
LEVEL_EXP_LENGTH = int(0.95 * SIDE_PANEL_LENGTH)
LEVEL_EXP_HEIGHT = int(SIDE_PANEL_HEIGHT / 21)


def draw_player_panel(player_name, refresh=False):
    """
    Renders the main window and player name.
    :param player_dict:
    :return: panel_rect, the rect that makes up the main panel
    """
    panel_rect = pg.Rect(PLAYER_PANEL_TOP_LEFT_X, PLAYER_PANEL_TOP_LEFT_Y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, panel_rect)
    pg.draw.rect(MAIN_WINDOW, colors.WHITE, panel_rect, 2)
    player_name = FONT_30.render(player_name, 1, colors.WHITE)
    MAIN_WINDOW.blit(player_name, (PLAYER_PANEL_TOP_LEFT_X + 5, PLAYER_PANEL_TOP_LEFT_Y + 5))

    return panel_rect


def draw_active_abilities(abilities, refresh=False, skill_points=0):
    """
    Renders the player's active abilities. If the ability is on cooldown, fill it with a darker color and also
    draw the number of turns left in the cooldown on the tile. If skill_points > 0, then draw a message telling
    the player that they have skill points to spend.
    """
    abilities_rect = pg.Rect(ABILITIES_TOP_LEFT_X, ABILITIES_TOP_LEFT_Y, ABILITY_TILE_LENGTH * 5, ABILITY_TILE_LENGTH)
    if refresh:
        MAIN_WINDOW.fill(color=colors.BLACK, rect=abilities_rect)
    while len(abilities) < 5:  # Pad the abilities list with None until it is of length 5
        abilities.append(None)
    abilities_label = FONT_20.render('ABILITIES', 1, colors.WHITE)
    MAIN_WINDOW.blit(abilities_label, (ABILITIES_TOP_LEFT_X, ABILITIES_TOP_LEFT_Y - 25))
    ability_tiles = list()
    for i, ability in enumerate(abilities):
        ability_tile = pg.Rect((i * ABILITY_TILE_LENGTH) + ABILITIES_TOP_LEFT_X, ABILITIES_TOP_LEFT_Y,
                               ABILITY_TILE_LENGTH, ABILITY_TILE_LENGTH)
        pg.draw.rect(MAIN_WINDOW, colors.GREY, ability_tile, 1)
        if ability is not None:
            ability_tiles.append(ability_tile)
            populate_ability_tile(ability, ability_tile)

        ability_number = FONT_20.render(str(i + 1), 1, colors.YELLOW)
        MAIN_WINDOW.blit(ability_number, (ABILITIES_TOP_LEFT_X + (1 + i) * ABILITY_TILE_LENGTH - 20,
                                          ABILITIES_TOP_LEFT_Y + ABILITY_TILE_LENGTH - 30))

    if skill_points > 0:
        skill_point_message = FONT_20.render(f"{skill_points} unspent skill point{'s' if skill_points > 1 else ''}, "
                                             f"press T to allocate", 1,
                                             colors.YELLOW)
        MAIN_WINDOW.blit(skill_point_message, (ABILITIES_TOP_LEFT_X, ABILITIES_TOP_LEFT_Y + 1.1 * ABILITY_TILE_LENGTH))

    return ability_tiles, abilities_rect


def populate_ability_tile(ability, ability_tile):
    """Adds color and cooldown timer to ability tile depending on if the ability is currently on cooldown."""
    if ability['turns_left'] > 0:  # Check if the ability is currently on cooldown
        turns_left_label = FONT_30.render(str(ability['turns_left']), 1, colors.WHITE)
        MAIN_WINDOW.fill(color=colors.DARK_BLUE, rect=(ability_tile[0] + 1, ability_tile[1] + 1,
                                                       ability_tile[2] - 2, ability_tile[3] - 2))
        MAIN_WINDOW.blit(turns_left_label, (ability_tile[0] + (ABILITY_TILE_LENGTH * 0.4),
                                            ability_tile[1] + (ABILITY_TILE_LENGTH * 0.2)))
    else:
        MAIN_WINDOW.fill(color=colors.BLUE, rect=(ability_tile[0] + 1, ability_tile[1] + 1,
                                                  ability_tile[2] - 2, ability_tile[3] - 2))


def draw_level_and_experience(level, profession, experience, refresh=False):
    """
    Renders the players level, type, and experience bar.
    :param level: An int which is the player's current level.
    :param profession: A string which is the player's current profession.
    :param experience: A list which stores the players experience progress as [current, max].
    :param refresh: A boolean which determines if the area around this info is filled to black, as a refresh.
    :return: The Rect enclosing all of the level and experience info.
    """
    level_and_exp_rect = pg.Rect(LEVEL_EXP_TOP_LEFT_X, LEVEL_EXP_TOP_LEFT_Y, LEVEL_EXP_LENGTH, LEVEL_EXP_HEIGHT)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, level_and_exp_rect)
    level_indicator = FONT_20.render(f"LEVEL {level} {profession.upper()}", 1, colors.WHITE)
    MAIN_WINDOW.blit(level_indicator, (LEVEL_EXP_TOP_LEFT_X, LEVEL_EXP_TOP_LEFT_Y))
    pg.draw.rect(MAIN_WINDOW, colors.GREY,
                 (LEVEL_EXP_TOP_LEFT_X, LEVEL_EXP_TOP_LEFT_Y + 24, LEVEL_EXP_LENGTH, LEVEL_EXP_HEIGHT - 27), 1)

    exp_percent = experience[0] / experience[1]
    current_exp_length = int(exp_percent * (SIDE_PANEL_LENGTH - 18 - PLAYER_PANEL_TOP_LEFT_X))
    if current_exp_length > 0:
        pg.draw.rect(MAIN_WINDOW, colors.PALE_YELLOW,
                     (LEVEL_EXP_TOP_LEFT_X, LEVEL_EXP_TOP_LEFT_Y + 26, current_exp_length, 6), 0)

    return level_and_exp_rect


def draw_attributes(attributes, level_up_points, refresh=False):
    """
    Renders the player's attributes.
    :param attributes: A dict containing all of the players attribute values.
    :param level_up_points: An int representing the number of level_up points the player has to allocate for their
                            attributes. If > 0, then the level-up buttons are also rendered
    :param refresh: A boolean determining if the area around this info is filled to black, as a refresh.
    :return: The Rect object enclosing the attributes.
    """
    attributes_rect = pg.Rect(PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 95, 150, 180)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, attributes_rect)
    coord_mapping = {
        'str': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 120),
        'dex': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 145),
        'int': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 170),
        'end': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 195),
        'vit': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 220),
        'wis': (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 245)
    }
    font = pg.font.Font(font_SIL, 20)
    for stat in coord_mapping:
        # Render the stat names and values separately, so that they can be properly aligned
        # TODO: Add logic to color stat values differently based on buffs/debuffs
        stat_name = font.render(f"{stat.upper()}: ", 1, colors.WHITE)
        stat_value = font.render(str(attributes[stat]), 1, colors.WHITE)
        MAIN_WINDOW.blit(stat_name, coord_mapping[stat])
        MAIN_WINDOW.blit(stat_value, (coord_mapping[stat][0] + 50, coord_mapping[stat][1]))

    if level_up_points > 0:
        draw_attribute_level_up_buttons(level_up_points)

    return attributes_rect


def draw_attribute_level_up_buttons(level_up_points, return_only=False):
    """
    Draws buttons next to player attributes for the purpose of allocating level-up points to increase attributes.
    :param level_up_points: Int, number of points available.
    :param return_only: Boolean, if True then don't draw anything, only return the list of button rects, to be used
                        for event-handling.
    :return: level_up_buttons, a list of Rect objects that make up all of the buttons.
    """
    top_left_x = PLAYER_PANEL_TOP_LEFT_X + 85
    top_left_y = PLAYER_PANEL_TOP_LEFT_Y + 125
    if not return_only:
        level_up_label = FONT_20.render(f"Points Available: {level_up_points}", 1, colors.GREY)
        MAIN_WINDOW.blit(level_up_label, (top_left_x - 75, top_left_y - 27))
    level_up_buttons = list()
    button_label = FONT_20.render("+", 1, colors.WHITE)
    for i in range(6):
        button_rect = pg.Rect(top_left_x, top_left_y + (i * 25), 20, 20)
        level_up_buttons.append(button_rect)
        if not return_only:
            MAIN_WINDOW.fill(color=colors.DARK_RED, rect=button_rect)
            MAIN_WINDOW.blit(button_label, (button_rect[0] + 4, button_rect[1]  - 5))

    return level_up_buttons


def draw_hp_mp(hp, mp, refresh=False):
    """
    Renders the player's HP and MP.
    :param hp: A list storing the player's current HP level as  [current, max]
    :param mp: A list storing the player's current MP level as  [current, max]
    :param refresh: As above.
    :return: The Rect object that encloses hp and mp.
    """
    hp_mp_rect = pg.Rect(PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 40, 100, 50)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, hp_mp_rect)
    hp_indicator = FONT_20.render("HP: {0} / {1}".format(hp[0], hp[1]), 1, colors.RED)
    mp_indicator = FONT_20.render("MP: {0} / {1}".format(mp[0], mp[1]), 1, colors.BLUE)
    MAIN_WINDOW.blit(hp_indicator, (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 40))
    MAIN_WINDOW.blit(mp_indicator, (PLAYER_PANEL_TOP_LEFT_X + 10, PLAYER_PANEL_TOP_LEFT_Y + 65))
    return hp_mp_rect


def draw_status(buffs, debuffs, refresh=False):
    """
    Draws indicators for player buffs and debuffs. Each will be represented by a 15x15 square, green for buffs and red
    for debuffs. Buffs will all go along one row, and debuffs along another row below.
    :param buffs: List of dict representations of every buff.
    :param debuffs: List of dict representations of every debuff.
    :param refresh: Same as above.
    :return: Lists of each rect for the buff and debuff indicators.
    """
    status_rect = pg.Rect(PLAYER_PANEL_TOP_LEFT_X + 130, PLAYER_PANEL_TOP_LEFT_Y + 40, 200, 50)
    if refresh:
        MAIN_WINDOW.fill(colors.BLACK, status_rect)
    buff_rects = list()
    debuff_rects = list()

    for i, buff in enumerate(buffs):
        buff_indicator = pg.Rect((i*17) + PLAYER_PANEL_TOP_LEFT_X + 130, PLAYER_PANEL_TOP_LEFT_Y + 40, 15, 15)
        buff_rects.append(buff_indicator)
        buff_turns_left = FONT_CALIBRI_12.render(str(buff['turns_left']), 1, colors.YELLOW)
        MAIN_WINDOW.blit(buff_turns_left, (buff_indicator[0] + 2, buff_indicator[1] + 2))
        pg.draw.rect(MAIN_WINDOW, colors.GREEN, buff_indicator, 1)

    for i, debuff in enumerate(debuffs):
        debuff_indicator = pg.Rect((i*17) + PLAYER_PANEL_TOP_LEFT_X + 130, PLAYER_PANEL_TOP_LEFT_Y + 57, 15, 15)
        debuff_rects.append(debuff_indicator)
        debuff_turns_left = FONT_CALIBRI_12.render(str(debuff['turns_left']), 1, colors.YELLOW)
        MAIN_WINDOW.blit(debuff_turns_left, (debuff_indicator[0] + 2, debuff_indicator[1] + 2))
        pg.draw.rect(MAIN_WINDOW, colors.RED, debuff_indicator, 1)

    return status_rect, buff_rects, debuff_rects


def draw_conditions(conditions, refresh=False):
    """
    Renders the player's current condition levels.
    :param conditions: A dict containing each condition and it's level as [current, max, counter]. Counter isn't
                       used in this module.
    :param refresh: As above.
    :return: The Rect object that encloses the conditions.
    """
    condition_rect = (PLAYER_PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - 90, PLAYER_PANEL_TOP_LEFT_Y + 10, 80, 90)
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
            condition_indicator = FONT_20.render(condition.upper(), 1, color)
            MAIN_WINDOW.blit(condition_indicator, (PLAYER_PANEL_TOP_LEFT_X + SIDE_PANEL_LENGTH - 90,
                                                   PLAYER_PANEL_TOP_LEFT_Y + condition_y_mapping[condition]))
    return pg.Rect(condition_rect)


def draw_inventory(inventory, refresh=False):
    """
    Draws the player inventory.
    :param inventory: A list of every Item object in the players inventory.
    :param refresh: As above.
    :return: inventory_tile, a list of every item rect in the inventory, and inventory_rect the rect of the whole
             inventory
    """
    inventory_rect = pg.Rect(INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y,
                             ITEM_LENGTH * int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS), ITEM_LENGTH * INVENTORY_NUM_ROWS)
    if refresh:
        MAIN_WINDOW.fill(color=colors.BLACK, rect=inventory_rect)
    inventory_label = FONT_20.render("INVENTORY", 1, colors.WHITE)
    MAIN_WINDOW.blit(inventory_label, (INVENTORY_TOP_LEFT_X, INVENTORY_TOP_LEFT_Y - 25))
    inventory_tiles = list()
    for y in range(INVENTORY_NUM_ROWS):
        for x in range(int(INVENTORY_LIMIT / INVENTORY_NUM_ROWS)):
            item_tile = pg.Rect((x * ITEM_LENGTH) + INVENTORY_TOP_LEFT_X,
                                (y * ITEM_LENGTH) + INVENTORY_TOP_LEFT_Y, ITEM_LENGTH, ITEM_LENGTH)
            pg.draw.rect(MAIN_WINDOW, colors.GREY, item_tile, 1)
            if len(inventory) >= (y * 6) + x + 1:
                MAIN_WINDOW.fill(color=colors.ORANGE, rect=((x * ITEM_LENGTH) + INVENTORY_TOP_LEFT_X + 1,
                                                            (y * ITEM_LENGTH) + INVENTORY_TOP_LEFT_Y + 1,
                                                            ITEM_LENGTH - 2, ITEM_LENGTH - 2))
                inventory_tiles.append(item_tile)
    return inventory_tiles, inventory_rect


def draw_equipment(equipment_dict, refresh=False):
    """
    Draws the players current equipment. Each equipment slot will be the size of an item tile in the inventory, arranged
    in a cross formation, e.g.
            X
           XXX
            X
    To do this, we render the equipment as a 3x3 grid, but only the squares that would appear in this cross are
    rendered, and the coordinates for this squares are mapped to the corresponding equipment slot in the
    grid_equipment_mapping dict below.
    :param equipment_dict: A dict containing the player's current equipment.
    :param refresh: As above.
    :return: equipment_tiles, a dict where the key is an equipment slot and the value is the Rect enclosing that slot,
             equipment_rect, a Rect object enclosing all of the equipment info.
    """
    equipment_rect = pg.Rect(EQUIPMENT_TOP_LEFT_X, EQUIPMENT_TOP_LEFT_Y, EQUIPMENT_LENGTH, EQUIPMENT_HEIGHT)
    if refresh:
        MAIN_WINDOW.fill(color=colors.BLACK, rect=equipment_rect)
    equipment_label = FONT_20.render("EQUIPMENT", 1, colors.WHITE)
    MAIN_WINDOW.blit(equipment_label, (EQUIPMENT_TOP_LEFT_X, EQUIPMENT_TOP_LEFT_Y - 8))
    grid_equipment_mapping = {
        (1, 0): 'head',
        (0, 1): 'hands',
        (1, 1): 'body',
        (2, 1): 'weapon',
        (1, 2): 'feet'
    }
    equipment_tiles = dict()
    for y in range(3):
        for x in range(3):
            if (x, y) not in grid_equipment_mapping:
                continue
            item_tile = pg.Rect((0.5 + x) * EQUIP_ITEM_LENGTH + EQUIPMENT_TOP_LEFT_X,
                                (0.5 + y) * EQUIP_ITEM_LENGTH + EQUIPMENT_TOP_LEFT_Y,
                                EQUIP_ITEM_LENGTH, EQUIP_ITEM_LENGTH)
            pg.draw.rect(MAIN_WINDOW, colors.GREY, item_tile, 1)
            # Check if the corresponding equipment slot currently has any items equipped.
            if equipment_dict[grid_equipment_mapping[(x, y)]]:
                MAIN_WINDOW.fill(color=colors.ORANGE, rect=((0.5 + x) * EQUIP_ITEM_LENGTH + EQUIPMENT_TOP_LEFT_X + 1,
                                                            (0.5 + y) * EQUIP_ITEM_LENGTH + EQUIPMENT_TOP_LEFT_Y + 1,
                                                            EQUIP_ITEM_LENGTH - 2, EQUIP_ITEM_LENGTH - 2))

            equipment_tiles[grid_equipment_mapping[(x, y)]] = item_tile
    return equipment_tiles, equipment_rect


def draw_item_details(item_dict, attributes_dict=None, current_equipment=None):
    """
    Function to draw a small window displaying item info. The top-left of the window will be determined by the position
    of the item in the inventory, so that the window will be enclosed by the inventory rectangle while also allowing
    the item to be invisible. Thus we have the window to appear to the left of the cursor if the item is in the right
    half of the inventory, and to the right of the cursor if the item is in the left half. The location of the mouse
    cursor is used to determine this.
    :param item_dict: A dict containing all of the item info necessary for rendering.
    :param attributes_dict: A dict containing the players current attributes, used only if the item is equipment.
    :param current_equipment: A dict containing the players current equipment, used only if the item is equipment.
    """

    mouse_pos = pg.mouse.get_pos()
    top_left_y = INVENTORY_TOP_LEFT_Y
    if mouse_pos[0] < PLAYER_PANEL_TOP_LEFT_X + int(SIDE_PANEL_LENGTH / 2):
        # Cursor is on the left side of the inventory
        top_left_x = mouse_pos[0]
    else:
        # Cursor is on the right side of the inventory
        top_left_x = mouse_pos[0] - ITEM_TOOLTIP_LENGTH

    # Body strings will be constructed differently for consumables and equipment.
    body_strings = list()
    if item_dict['type'] == 'consumable':
        body_strings = item_dict['description'] + ['---'] + item_dict['details'] + ['---', 'Left-click to consume']

    elif item_dict['type'] == 'equipment':
        # In this case we outsource the logic to another function, since it is a lot of logic.
        body_strings = parse_equipment_details(item_dict, attributes_dict, current_equipment)

    draw_detail_window(body_strings=body_strings, location='player_panel',
                       rect_dimensions=(top_left_x, top_left_y, ITEM_TOOLTIP_LENGTH, ITEM_TOOLTIP_HEIGHT),
                       header_string=item_dict['name'].upper(), auto_window_height=True, auto_window_width=True)


def draw_equipment_details(equipment_dict, slot):
    """
    Draws tooltip with equipment info if there is an item equipped in the slot being moused over, or draws a tooltip
    detailing the slot if no item is equipped. Tooltip will always be drawn to the left of the mouse.
    """
    mouse_pos = pg.mouse.get_pos()
    top_left_y = mouse_pos[1]
    top_left_x = mouse_pos[0] - ITEM_TOOLTIP_LENGTH
    if equipment_dict:  # i.e. if the item in the equipment slot is not None
        body_strings = equipment_dict['description'] + ['---']
        if equipment_dict['off_rating'] > 0:
            body_strings.append(f"OFF {equipment_dict['off_rating']}")
        else:
            body_strings.append(f"DEF {equipment_dict['def_rating']}")
        header_string = equipment_dict['name'].upper()

    else:
        body_strings = ['Nothing equipped here.']
        header_string = slot.upper()

    draw_detail_window(body_strings=body_strings, location='player_panel',
                       rect_dimensions=(top_left_x, top_left_y, ITEM_TOOLTIP_LENGTH, ITEM_TOOLTIP_HEIGHT),
                       header_string=header_string, auto_window_width=True, auto_window_height=True)


def parse_equipment_details(item_dict, attributes_dict, current_equipment):
    """
    Function to parse equipment details and player attributes to draw the detail text correctly, with appropriate colors
    and whatnot. If the player doesn't meat the stat requirements, the string of requirements will be red. Then
    we check if the item has better offense then what's equipped (if a weapon) or better defense (if armor), and if the
    new item is an upgrade then the text displaying this will be green, if worse it will be red, and if equal it will be
    white.
    :param item_dict: Dict containing item details.
    :param attributes_dict: Dict containing player's attribute details, to see if they meet stat requirements.
    :param current_equipment: Dict containing player's current equipment, to see if this equipment is an upgrade.
    :return: body_strings, a list of strings to be rendered.
             body_colors, a list of the corresponding color each string should render in.
    """
    if not attributes_dict:
        raise Exception(f"No attributes for equipment detail window: {item_dict['name']}")
    # Initialize body_strings as the item description (already a list) and all in white.
    body_strings = [(string, colors.WHITE) for string in item_dict['description'] + ['---']]
    if item_dict['stat_req']:
        requirement_color = colors.WHITE
        requirement_string = 'REQ: '
        for stat in item_dict['stat_req']:
            requirement_string += f"{item_dict['stat_req'][stat]} {stat.upper()}   "
            if attributes_dict[stat] < item_dict['stat_req'][stat]:
                requirement_color = colors.RED
        body_strings.append((requirement_string.strip(), requirement_color))
    # If item is a weapon we compare the off_rating, else we compare the def rating
    stat_to_compare = 'off_rating' if item_dict['off_rating'] > 0 else 'def_rating'
    compare_color = colors.GREEN
    # If no item is currently equipped in the slot, then the color defaults to green since it must be an
    # upgrade. If there is an item equipped, we check to see if it could be worse or equal, so as to change the color.
    if current_equipment.get(item_dict['slot'], None):
        current_equipment_info = current_equipment[item_dict['slot']].to_dict()
        if item_dict[stat_to_compare] < current_equipment_info[stat_to_compare]:
            compare_color = colors.RED
        elif item_dict[stat_to_compare] == current_equipment_info[stat_to_compare]:
            compare_color = colors.WHITE
    # The weird string in the first format maps 'off_rating' to 'OFF' and 'def_rating' to 'DEF'.
    body_strings.append((f"{stat_to_compare[:3].upper()} {item_dict[stat_to_compare]}", compare_color))
    body_strings.extend(['---', 'Left-click to equip'])

    return body_strings


def draw_condition_details(conditions_dict, conditions_rect):
    """
    CURRENTLY NOT IN USE
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

    draw_detail_window(body_strings=window_body, rect_dimensions=(top_left_x, top_left_y, width, height), font_size=15,
                       location='player_panel')


def draw_status_details(status):
    """Function to draw a tooltip providing details on the status currently being hovered over."""
    window_body = ['----'] + status['description'] + ['----', f'Expires in {status["turns_left"]} turns.']
    draw_detail_window(header_string=status['name'], body_strings=window_body, location='player_panel',
                       rect_dimensions=(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], ITEM_TOOLTIP_LENGTH,
                                        ITEM_TOOLTIP_HEIGHT))


def draw_ability_details(ability, player_attributes, player_mp=None):
    """
    Draws tooltip showing details on currently moused-over ability. If the mouse is to the left of the center of the
    player panel, display the tooltip to the right of the cursor, and vice-versa. Also, the tooltip will display
    above the cursor regardless of mouse position. If player_mp is None, this implies that the function was called from
    the skill tree, so we don't display info such as turns left in the cooldown.
    """
    mouse_pos = pg.mouse.get_pos()
    if mouse_pos[0] > PLAYER_PANEL_TOP_LEFT_X + int(SIDE_PANEL_LENGTH / 2):
        top_left_x = mouse_pos[0] - ITEM_TOOLTIP_LENGTH
    else:
        top_left_x = mouse_pos[0]
    if mouse_pos[1] > PLAYER_PANEL_TOP_LEFT_Y + int(SIDE_PANEL_HEIGHT / 2):
        top_left_y = mouse_pos[1] - (1.5 * ITEM_TOOLTIP_HEIGHT)
    else:
        top_left_y = mouse_pos[1]
    parsed_description = parse_description(ability['description'], char_limit=33)
    window_body = ['----', f'{"ACTIVE" if ability["active"] else "PASSIVE"} SKILL'] + parsed_description + \
                  ['----', f'Level: {max(ability["level"], 1)}']
    # Ability details are stored in a dict, where each key-value pair looks something like
    #    'HP Regen Per Turn' : '{skill_level} + {wis} * 2'
    # So we use format() with the skill level and player attributes to fill in the values, and eval() to evaluate
    # the string expression to an integer value. If the skill is level 0 (not allocated), show the details for level 1
    window_body += [f'{key}: {eval(value.format(skill_level=max(ability["level"], 1), **player_attributes))}'
                    for key, value in ability['details'].items()]
    if player_mp is not None:  # Implies tooltip is being displayed in the player panel
        if ability['turns_left'] > 0:  # Only display 'turns left' info if the ability is on cooldown
            window_body.append(f'Turns left on cooldown: {ability["turns_left"]}')
        if ability['mp_cost'] > player_mp[0]:
            window_body.append(("Not enough MP!!", colors.RED))
    elif 0 < ability['level'] < 3: # Implies this is being displayed in the skill tree (since player_mp is None)
        # If the ability level is in (0, 3) we show the details for the next level as well.
        window_body += ['----', 'Next Level:'] +\
                       [f'{key}: {eval(value.format(skill_level=ability["level"] + 1, **player_attributes))}'
                        for key, value in ability['details'].items()]
    draw_detail_window(header_string=ability['name'], body_strings=window_body, auto_window_height=True,
                       rect_dimensions=(top_left_x, top_left_y, 1.05 * ITEM_TOOLTIP_LENGTH, 1.5 * ITEM_TOOLTIP_HEIGHT),
                       location='player_panel')


def draw_exp_details(experience):
    """Draws tooltip showing details about the player's current experience progress."""
    window_body = [f'Experience: {experience[0]} / {experience[1]}']
    mouse_pos = pg.mouse.get_pos()
    length = int(0.4*SIDE_PANEL_LENGTH)
    if mouse_pos[0] > PLAYER_PANEL_TOP_LEFT_X + int(SIDE_PANEL_LENGTH / 2):
        top_left_x = mouse_pos[0] - length
    else:
        top_left_x = mouse_pos[0]
    top_left_y = mouse_pos[1]
    draw_detail_window(body_strings=window_body,
                       rect_dimensions=(top_left_x, top_left_y, length, 30), location='player_panel')


