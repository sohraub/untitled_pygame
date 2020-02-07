import pygame as pg

import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL


class PlayerPanel:
    def __init__(self, game):
        self.game = game
        self.top_left_x = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2)
        self.top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)


    def refresh_hp_mp(self):
        self.game.window.fill(colors.BLACK,
                              (self.top_left_x + 10, self.top_left_y + 40, self.top_left_x + 100, 50))
        self.draw_conditions(just_refresh_hp_mp=True)

    def draw_conditions(self, just_refresh_hp_mp=False):
        hp_string = "HP: {0} / {1}".format(self.game.player.hp[0], self.game.player.hp[1])
        mp_string = "MP: {0} / {1}".format(self.game.player.mp[0], self.game.player.mp[1])
        font = pg.font.Font(font_SIL, 20)
        hp_indicator = font.render(hp_string, 1, colors.RED)
        mp_indicator = font.render(mp_string, 1, colors.BLUE)
        self.game.window.blit(hp_indicator, (self.top_left_x + 10, self.top_left_y + 40))
        self.game.window.blit(mp_indicator, (self.top_left_x + 10, self.top_left_y + 65))
        if not just_refresh_hp_mp:
            for condition in ['tired', 'hungry', 'thirsty']:
                if self.game.player.condition[condition][0] < 0.5 * self.game.player.condition[condition][1]:
                    self.display_condition_state(condition)


    def display_condition_state(self, condition):
        condition_y_mapping = {'thirsty': 10, 'hungry': 35, 'tired': 60}
        current = self.game.player.condition[condition][0]
        max = self.game.player.condition[condition][1]
        if current < 0.15 * max:
            color = colors.RED
        elif current < 0.35 * max:
            color = colors.ORANGE
        else:
            color = colors.YELLOW
        font = pg.font.Font(font_SIL, 20)
        condition_indicator = font.render(condition.upper(), 1, color)
        self.game.window.blit(condition_indicator, (self.top_left_x + SIDE_PANEL_LENGTH - 90,
                                          self.top_left_y + condition_y_mapping[condition]))


    def display_attributes(self):
        coord_mapping = {
            'str': (self.top_left_x + 10, self.top_left_y + 120),
            'dex': (self.top_left_x + 10, self.top_left_y + 145),
            'int': (self.top_left_x + 10, self.top_left_y + 170),
            'end': (self.top_left_x + 120, self.top_left_y + 120),
            'vit': (self.top_left_x + 120, self.top_left_y + 145),
            'wis': (self.top_left_x + 120, self.top_left_y + 170)
        }
        font = pg.font.Font(font_SIL, 20)
        for stat in coord_mapping.keys():
            string = "{0}: {1}".format(stat.upper(), self.game.player.attributes[stat])
            stat_indicator = font.render(string, 1, colors.WHITE)
            self.game.window.blit(stat_indicator, coord_mapping[stat])


    def draw_level_and_experience(self):
        font = pg.font.Font(font_SIL, 20)
        level_indicator = font.render("LEVEL {} {}".format(self.game.player.level, self.game.player.type.upper()),
                                      1, colors.WHITE)
        self.game.window.blit(level_indicator, (self.top_left_x + 10, self.top_left_y + 220))
        pg.draw.rect(self.game.window, colors.GREY,
                     (self.top_left_x + 6, self.top_left_y + 248, SIDE_PANEL_LENGTH - 12, 8), 1)
        exp_percent = self.game.player.experience[0] / self.game.player.experience[1]
        current_exp_length = int(exp_percent * (SIDE_PANEL_LENGTH - 18 - self.top_left_x))
        if current_exp_length > 0:
            pg.draw.rect(self.game.window, colors.PALE_YELLOW,
                         (self.top_left_x + 7, self.top_left_y + 249, current_exp_length, 6), 0)


    def draw_player_panel(self):
        pg.draw.rect(self.game.window, colors.WHITE,
                     (self.top_left_x, self.top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)
        font = pg.font.Font(font_SIL, 30)
        self.game.player_name = font.render(self.game.player.name, 1, colors.WHITE)
        self.game.window.blit(self.game.player_name, (self.top_left_x + 5, self.top_left_y + 5))
        self.draw_conditions()
        self.display_attributes()
        self.draw_level_and_experience()



