import pygame as pg

import colors
from config import TOP_LEFT_X, PLAY_LENGTH, font_SIL
"""
Class for the console that will display text based on what is happening in the game.
"""

class Console:
    def __init__(self):
        self.lines = ['', '', '', '']

    def update_console(self, new_lines):
        for new_line in new_lines:
            self.lines.pop(0)
            self.lines.append(new_line)
        self.refresh_console()

    def refresh_console(self):
        self.window.fill(colors.BLACK, rect=(TOP_LEFT_X, 25, PLAY_LENGTH, (25 + (3 * 16))))
        font = pg.font.Font(font_SIL, 15)
        for i, line in enumerate(self.lines):
            line_render = font.render(line, 1, colors.WHITE)
            self.window.blit(line_render, (TOP_LEFT_X, 25 + (i * 16)))

