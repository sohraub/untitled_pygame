import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE,\
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, SHADOWS_INTO_LIGHT


class MiscPanel:
    def __init__(self, game, focus_tile=None):
        self.game = game
        self.focus_tile = focus_tile
        self.top_left_x = WINDOW_LENGTH - ((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2) - SIDE_PANEL_LENGTH
        self.top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)
        self.f_window_top_left_x = self.top_left_x + int(0.02*SIDE_PANEL_LENGTH)  # Top-left coords for the focus window
        self.f_window_top_left_y = self.top_left_y + int(0.02*SIDE_PANEL_HEIGHT)
        self.f_window_length = int(0.96*SIDE_PANEL_LENGTH)
        self.f_window_height = int(0.3*SIDE_PANEL_HEIGHT)


    def draw_misc_panel(self):
        pg.draw.rect(self.game.window, colors.WHITE,
                     (self.top_left_x, self.top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
        self.draw_focus_window()


    def draw_focus_window(self):
        f_window_rect = (self.f_window_top_left_x, self.f_window_top_left_y, self.f_window_length, self.f_window_height)
        pg.draw.rect(self.game.window, colors.WHITE, f_window_rect, 1)
        # Re-fill the area just inside the window to black, as a refresh
        self.game.window.fill(colors.BLACK,
                              rect=(f_window_rect[0]+1, f_window_rect[1]+1, f_window_rect[2]-2, f_window_rect[3]-2))
        if self.focus_tile is not None:
            # This mapping gives the appropriate function to load data, based on the type of tile which under focus
            focus_function_mapping = {
                'E': self.load_enemy_info
            }
            # Get the letter representation of the tile from the board template
            tile_type = self.game.board.template[self.focus_tile[1]][self.focus_tile[0]]
            focus_function_mapping[tile_type]()


    def load_enemy_info(self):
        enemy = self.game.board.enemies[self.focus_tile]
        portrait_top_left_x = self.f_window_top_left_x + int(0.025*self.f_window_length)
        portrait_top_left_y = self.f_window_top_left_y + int(0.025*self.f_window_height)
        portrait_length = int(0.19*self.f_window_length)
        portrait_height = int(0.3*self.f_window_height)
        pg.draw.rect(self.game.window, colors.WHITE,
                     (portrait_top_left_x, portrait_top_left_y, portrait_length, portrait_height), 1)

        big_font = pg.font.Font(SHADOWS_INTO_LIGHT, 30)
        small_font = pg.font.Font(SHADOWS_INTO_LIGHT, 15)

        enemy_hp_percentage = float(enemy.hp[0]) / float(enemy.hp[1])
        if enemy_hp_percentage > 0.66:
            health_text = 'This creature looks quite healthy.'
        elif enemy_hp_percentage > 0.33:
            health_text = 'This creature seems to be in pain.'
        else:
            health_text = 'This creature is on the brink of death.'

        enemy_name = big_font.render(' '.join(enemy.name.split('_')[0:-1]).upper(), 1, colors.WHITE)
        flavour_text = small_font.render(enemy.flavour_text, 1, colors.WHITE)
        health_indicator = small_font.render(health_text, 1, colors.WHITE)

        self.game.window.blit(enemy_name, (portrait_top_left_x + portrait_length + 5, portrait_top_left_y))
        self.game.window.blit(flavour_text, (portrait_top_left_x, portrait_top_left_y + portrait_height + 3))
        self.game.window.blit(health_indicator, (portrait_top_left_x, portrait_top_left_y + portrait_height + 45))

