import pygame as pg

import colors
from config import TOP_LEFT_X, PLAY_LENGTH, font_SIL
from rendering.window_renderer import MAIN_WINDOW, FONT_15

def render_console(lines):
    MAIN_WINDOW.fill(colors.BLACK, rect=(TOP_LEFT_X - 20, 16, PLAY_LENGTH, (25 + (5 * 16))))
    for i, line in enumerate(lines):
        # Add an effect so that most recent lines in the console are brightest, and oldest get gradually darker
        color_offset = 25 * (len(lines) - i)
        color = (colors.WHITE[0] - color_offset, colors.WHITE[1] - color_offset, colors.WHITE[2] - color_offset)
        line_render = FONT_15.render(line, 1, color)
        MAIN_WINDOW.blit(line_render, (TOP_LEFT_X - 20, 16 + (i * 16)))

