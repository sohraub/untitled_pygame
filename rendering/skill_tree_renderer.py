import pygame as pg

import colors

from config import WINDOW_HEIGHT, TOP_LEFT_X, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from rendering.window_renderer import MAIN_WINDOW, FONT_15, FONT_20, FONT_30, FONT_TNR_12, draw_detail_window
from rendering.player_panel_renderer import PANEL_TOP_LEFT_X, PANEL_TOP_LEFT_Y, ABILITY_TILE_LENGTH, draw_ability_details



def draw_skill_tree(active_abilities, passive_abilities, skill_tree, profession, player_level, skill_points):
    """
    Draws the character's skill tree in the player panel. Skill trees will be made of 7 layers, each layer alternating
    between active and passive skills. Extra rendering logic is added to the layers with active abilities after the
    first, so that a piece of text saying "OR" will appear between the skills, to indicate that the player can only
    choose one active skill for each layer after the first. All the parameters are taken from the player_dict saved
    as an attribute in the PlayerPanel class.
    :param active_abilities: List of the Player's current active abilities
    :param passive_abilities: List of the Player's current passive abilities
    TODO: Do we need the two above lists? Can all the info we need just be gleaned from the skill tree?
    :param profession: String, the Player's profession
    :param skill_tree: Nested dict of the Player's skill tree
    :param skill_points: Int, number of skill points the player has to allocate
    :return: rect_map, a dict that has as keys the name of the tree level and index in the level, and it's value is the
             corresponding rect. E.g., the entry for the 2nd skill in the active_2 row would have the entry:
                ('active_2', 1) : pg.Rect(...)
    """
    # Reset the player panel to black.
    MAIN_WINDOW.fill(color=colors.BLACK,
                     rect=(PANEL_TOP_LEFT_X + 1, PANEL_TOP_LEFT_Y + 1, SIDE_PANEL_LENGTH - 2, SIDE_PANEL_HEIGHT - 2))

    skill_tile_length = 0.7 * ABILITY_TILE_LENGTH
    space_between_levels = 0.9 * skill_tile_length  # The vertical space between each layer of the tree
    draw_skill_tree_level_progression(player_level, space_between_levels, skill_tile_length)
    # Render the title of the skill tree, PATH OF THE {profession}
    skill_tree_title = FONT_20.render(f'PATH OF THE {profession.upper()}', 1, colors.WHITE)
    MAIN_WINDOW.blit(skill_tree_title, (PANEL_TOP_LEFT_X + 5, PANEL_TOP_LEFT_Y + 5))
    points_remaining = FONT_20.render(f'Skill points remaining: {skill_points}', 1, colors.WHITE)
    MAIN_WINDOW.blit(points_remaining, (PANEL_TOP_LEFT_X + 5, PANEL_TOP_LEFT_Y + 30))
    rect_map = dict()
    for tree_level, level_name in enumerate(skill_tree):
        num_skills_in_row = len(skill_tree[level_name])
        # Horizontal space between skills within a layer will be based off the number of skills in each layer
        space_between_skills = (SIDE_PANEL_LENGTH - (num_skills_in_row * skill_tile_length)) / (num_skills_in_row + 1)
        for i in range(num_skills_in_row):
            # This formula for the top-left xy-coordinates of each skill works out such that the space between each
            # skill in a row will come out equal to space_between_skills, and the vertical space between each layer
            # will be space_between_levels
            skill_rect = ((i + 1) * space_between_skills + i * skill_tile_length + PANEL_TOP_LEFT_X,
                          (tree_level + 1) * space_between_levels + tree_level * skill_tile_length + PANEL_TOP_LEFT_Y + 40,
                          skill_tile_length, skill_tile_length)
            rect_map[(level_name, i)] = pg.Rect(skill_rect)
            pg.draw.rect(MAIN_WINDOW, colors.GREY, skill_rect, 0 if skill_tree[level_name][i]['skill_level'] > 0 else 1)
            if level_name in {'active_2', 'active_3', 'active_4'} and i > 0:
                # On the active skill layers (excluding the first), render an 'OR' between each skill. Location of the
                # text will be calculated based on the top-left coordinates of the skill that will appear after it
                # in a left-to-right order.
                MAIN_WINDOW.blit(FONT_20.render('OR', 1, colors.RED),
                                 (skill_rect[0] - 0.54 * space_between_skills - 10,
                                  skill_rect[1] + 0.2 * space_between_levels))

    return rect_map


def draw_skill_tree_level_progression(player_level, space_between_levels, skill_tile_length):
    """
    Draws a margin on the skill tree displaying the required player level for each tree level, as well as filling in
    the background of the tree to indicate what level the player has reached so far.
    The required player level will be displayed in a badge icon (think an upside-down pentagon), which will be drawn
    by passing in a list of 5 xy-coordinate pairs to the draw_polygon() pygame function. The x and y variables below
    refer to the x and y coordinate values of the top-left corner of the first badge, from which all other points will
    be derived.
    """
    MAIN_WINDOW.fill(color=colors.DARK_RED,
                     rect=(PANEL_TOP_LEFT_X + 1, PANEL_TOP_LEFT_Y + 1, SIDE_PANEL_LENGTH - 2,
                           min(player_level * (space_between_levels + skill_tile_length) + 40, SIDE_PANEL_HEIGHT - 2)))
    x = PANEL_TOP_LEFT_X + 0.3  * skill_tile_length
    y = PANEL_TOP_LEFT_Y + 2 * skill_tile_length
    badge_length = 0.3 * skill_tile_length
    base_badge_points = [(x, y), (x + badge_length, y), (x + badge_length, y + badge_length),
                         (x + 0.5 * badge_length, y + 1.5 * badge_length), ( x, y + badge_length)]
    req_level_from_tree_level = {
        0: '1',
        1: '2',
        2: '4',
        3: '5',
        4: '7',
        5: '8',
        6: '10'
    }
    for i in range(7):
        badge_points = [(a, b + i * (skill_tile_length + space_between_levels)) for (a, b) in base_badge_points]
        pg.draw.polygon(MAIN_WINDOW, colors.YELLOW, badge_points)
        level_text = FONT_TNR_12.render(req_level_from_tree_level[i], 1, colors.BLACK)
        text_rect = level_text.get_rect(center=(badge_points[0][0] + 0.5 * badge_length,
                                                badge_points[0][1] + 0.75* badge_length))
        MAIN_WINDOW.blit(level_text, text_rect)


def draw_ability_details_in_skill_tree(ability):
    """
    Draws tooltips in the skill tree displaying info for the ability currently being moused over. Position of the
    window depends on the mouse location, e.g. if the mouse is on the top half of the screen, then display the window
    downwards, or if the mouse is on the left side of the panel display the window to the right of the cursor, etc.
    """
    draw_ability_details(ability.to_dict())
