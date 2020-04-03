import pygame as pg

import colors
from config import TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT
from rendering.window_renderer import MAIN_WINDOW, FONT_15

def render_console(lines):
    """
    Prints every line in 'lines' to the console at the top of the screen.
    :param lines: A list of strings.
    :return: n/a
    """
    #TODO: Re-do dimensions in terms of config variables
    console_rect = (TOP_LEFT_X * 0.956, TOP_LEFT_Y * 0.128, PLAY_LENGTH, TOP_LEFT_Y * 0.84)
    MAIN_WINDOW.fill(colors.BLACK, rect=console_rect)
    for i, line in enumerate(lines):
        # Add an effect so that most recent lines in the console are brightest, and oldest get gradually darker
        color_offset = 25 * (len(lines) - i)
        color = (colors.WHITE[0] - color_offset, colors.WHITE[1] - color_offset, colors.WHITE[2] - color_offset)
        line_render = FONT_15.render(line, 1, color)
        MAIN_WINDOW.blit(line_render, (TOP_LEFT_X - 20, 16 + (i * 16)))
        pg.display.update(console_rect)


