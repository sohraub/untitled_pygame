import os
import pygame as pg

import colors
from config import WINDOW_HEIGHT, WINDOW_LENGTH, font_SIL

"""
Module that initializes pygame and the rendering of the game window. Holds the MAIN_WINDOW surface which every 
subsequent rendering method draws upon. Also holds the font objects that are imported into rendering modules, and some
general functions that are useful for all rendering modules.
"""

os.environ['SDL_VIDEO_WINDOW_POS'] = "25, 45"
pg.init()
MAIN_WINDOW = pg.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
MAIN_WINDOW.fill(colors.BLACK)
pg.display.set_caption('Untitled Game #1')

# Font objects. Default font used is Shadows_into_light, with Times New Roman used for some small text.
FONT_50 = pg.font.Font(font_SIL, 50)
FONT_30 = pg.font.Font(font_SIL, 30)
FONT_25 = pg.font.Font(font_SIL, 25)
FONT_20 = pg.font.Font(font_SIL, 20)
FONT_15 = pg.font.Font(font_SIL, 15)
FONT_10 = pg.font.Font(font_SIL, 10)
FONT_CALIBRI_12 = pg.font.SysFont('calibri', 12)
FONT_CALIBRI_13 = pg.font.SysFont('calibri', 13)

def draw_detail_window(body_strings, rect_dimensions, header_string=None, window_color=colors.NAVY, font_size=13,
                       auto_window_height=False, auto_window_width=False):
    """
    Draws a small window giving more info on any arbitrary thing in the game, usually called on mouseover of that thing.
    :param header_string: The main header of the detail window, a string.
    :param body_strings: The body of the details window, a list of (string, color) tuples. If an entry is just a string,
                         it will be set to a tuple of (string, colors.WHITE).
    :param rect_dimensions: Dimensions for the window, given in a tuple as (top-left-x, top-left-y, width, height).
    :param window_color: The color for the window, defaulting to navy.
    :param font_size: The size of the font used in the body. If default, use size 13.
    :param auto_window_height: Boolean, default to False. If true, automatically determine the height of the tooltip
                                based on the number of lines and existence of a header.
    :param auto_window_width: Boolean, default to False. If true, automatically determine the width of the tooltip based
                              on the length of the longest line in body_strings and header_string.
    :return: n/a
    """
    if auto_window_height or auto_window_height:
        rect_dimensions = find_auto_dimensions(auto_window_height, auto_window_width, rect_dimensions, body_strings,
                                               header_string, font_size)
    MAIN_WINDOW.fill(window_color, rect_dimensions)
    # If no header is given, this offset will be set at 2 so that there is no blank space at the top.
    body_offset = 2
    if header_string is not None:
        # If a header is given, render that at the top of the window and offset the body by 27 pixels.
        body_offset = 35
        header = FONT_20.render(header_string, 1, colors.WHITE)
        MAIN_WINDOW.blit(header, (rect_dimensions[0] + 5, rect_dimensions[1] + 2))
    body_font = pg.font.SysFont('calibri', font_size)
    for i, entry in enumerate(body_strings):
        if type(entry) != tuple:
            body_strings[i] = (entry, colors.WHITE)
    body = [body_font.render(string, 1, color) for (string, color) in body_strings]
    # The first two elements of rect_dimensions correspond to the top_left_x and top_left_y of the window, resp.
    for i, string in enumerate(body):
        MAIN_WINDOW.blit(string, (rect_dimensions[0] + 10, rect_dimensions[1] + body_offset + 16*i))


def find_auto_dimensions(auto_height, auto_width, rect_dimensions, body_strings, header_string, font_size):
    """
    Returns dimensions of tooltip window after determining width and/or height automatically. Height will be based on
    number of lines in body_strings, font_size, and presence of a header. Width will be based on the length of the
    longest line between the body strings and header string, account for font size as well.
    """
    if auto_height:
        auto_height = (font_size + 4) * len(body_strings)  # Add 4 to account for whitespace between lines.
        auto_height += 35 if header_string is not None else 10
        rect_dimensions = (rect_dimensions[0], rect_dimensions[1], rect_dimensions[2], auto_height)
    if auto_width:
        max_width = 0
        for line in body_strings:
            if type(line) == tuple:  # Handle cases where body string is a tuple of (string, color)
                line = line[0]
            # Multiple font_size by 0.5 since letters are approx. half as wide as they are tall.
            max_width = max(max_width, len(line) * (0.45 * font_size))
        max_width = max(max_width, len(header_string) * 12) if header_string is not None else max_width
        rect_dimensions = (rect_dimensions[0], rect_dimensions[1], max_width, rect_dimensions[3])

    return rect_dimensions