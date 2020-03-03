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
FONT_TNR_15 = pg.font.SysFont('timesnewroman', 13)


def draw_detail_window(header_string, body_strings, rect_dimensions, window_color=colors.NAVY):
    MAIN_WINDOW.fill(window_color, rect_dimensions)
    header = FONT_20.render(header_string, 1, colors.WHITE)
    body = [FONT_TNR_15.render(string, 1, colors.WHITE) for string in body_strings]
    # The first two elements of rect_dimensions correspond to the top_left_x and top_left_y of the window, resp.
    MAIN_WINDOW.blit(header, (rect_dimensions[0] + 2, rect_dimensions[1] + 2))
    for i, string in enumerate(body):
        MAIN_WINDOW.blit(string, (rect_dimensions[0] + 5, rect_dimensions[1] + 27 + 16*i))