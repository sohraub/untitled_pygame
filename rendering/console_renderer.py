import pygame as pg

import colors
from config import TOP_LEFT_X, PLAY_LENGTH, font_SIL
from rendering.window_renderer import MAIN_WINDOW, FONT_15

def render_console(lines):
    MAIN_WINDOW.fill(colors.BLACK, rect=(TOP_LEFT_X, 25, PLAY_LENGTH, (25 + (3 * 16))))
    for i, line in enumerate(lines):
        line_render = FONT_15.render(line, 1, colors.WHITE)
        MAIN_WINDOW.blit(line_render, (TOP_LEFT_X, 25 + (i * 16)))
