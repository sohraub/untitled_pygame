import pygame as pg

import colors
from config import WINDOW_HEIGHT, WINDOW_LENGTH, font_SIL

"""
Module that initializes pygame and the rendering of the game window. Holds the MAIN_WINDOW surface which every 
subsequent rendering method draws upon. Also holds the font objects that are imported into rendering modules, and some
general functions that are useful for all rendering modules.
"""

pg.init()
MAIN_WINDOW = pg.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
MAIN_WINDOW.fill(colors.BLACK)
pg.display.set_caption('Untitled Game #1')

# Font objects. Default font used is Shadows_into_light, with Times New Roman used for some small text.
FONT_30 = pg.font.Font(font_SIL, 30)
FONT_25 = pg.font.Font(font_SIL, 25)
FONT_20 = pg.font.Font(font_SIL, 20)
FONT_15 = pg.font.Font(font_SIL, 15)
FONT_10 = pg.font.Font(font_SIL, 10)
FONT_TNR_12 = pg.font.SysFont('timesnewroman', 12)
FONT_TNR_13 = pg.font.SysFont('timesnewroman', 13)


def draw_detail_window(body_strings, rect_dimensions, header_string=None, window_color=colors.NAVY, body_colors=None,
                       font_size=13):
    """
    Draws a small window giving more info on any arbitrary thing in the game, usually called on mouseover of that thing.
    :param header_string: The main header of the detail window, a string.
    :param body_strings: The body of the details window, a list of strings.
    :param rect_dimensions: Dimensions for the window, given in a tuple as (top-left-x, top-left-y, width, height).
    :param window_color: The color for the window, defaulting to navy.
    :param body_colors: A list containing a color for each line in body_strings. If None, gets set to all white.
    :param font_size: The size of the font used in the body. If default, use size 15.
    :return: n/a
    """
    MAIN_WINDOW.fill(window_color, rect_dimensions)
    # If no header is given, this offset will be set at 2 so that there is no blank space at the top.
    body_offset = 2
    if header_string is not None:
        # If a header is given, render that at the top of the window and offset the body by 27 pixels.
        body_offset = 27
        header = FONT_20.render(header_string, 1, colors.WHITE)
        MAIN_WINDOW.blit(header, (rect_dimensions[0] + 2, rect_dimensions[1] + 2))
    body_font = pg.font.SysFont('timesnewroman', font_size)
    if body_colors is None:
        body_colors = [colors.WHITE for _ in body_strings]
    else:
        if len(body_colors) != len(body_strings):
            # If body_colors is not None, it has to be the same size as body_strings.
            raise Exception("Length of body_strings and body_colors don't match.")
    body = [body_font.render(string, 1, color) for string,color in zip(body_strings, body_colors)]
    # The first two elements of rect_dimensions correspond to the top_left_x and top_left_y of the window, resp.
    for i, string in enumerate(body):
        MAIN_WINDOW.blit(string, (rect_dimensions[0] + 5, rect_dimensions[1] + body_offset + 16*i))