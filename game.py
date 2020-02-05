import pygame as pg

import player_panel
import misc_panel
import colors

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, SHADOWS_INTO_LIGHT
from game_elements.element_config_values import BOARD_HEIGHT, BOARD_LENGTH
from game_elements.board import Board
from game_elements.player import Player


class Game:
    def __init__(self, window, board=None, player=None, filename='untitlted'):
        self.window = window
        self.board = board if board is not None else Board()
        self.player = player if player is not None else Player()
        self.player.x = self.board.player_coordinates[0]
        self.player.y = self.board.player_coordinates[1]
        self.filename = filename


    def move_player_on_board(self, input):
        """
        Given a basic movement input, moves the player character and updates its position
        on the board
        """
        old_x = self.player.x
        old_y = self.player.y
        new_x, new_y = self.player.perform_movement(input)
        if self.board.template[new_y][new_x] == 'O':  # Checks if player is moving to an open tile
            self.board.player_coordinates = (new_x, new_y)
            self.board.rebuild_template()
        else:
            self.player.x = old_x
            self.player.y = old_y
            if self.board.template[new_y][new_x] == 'E':  # Moving to a tile which contains an enemy attacks the enemy
                self.refresh_focus_window((new_x, new_y))
                target_enemy = self.board.enemies[(new_x, new_y)]
                print(target_enemy.hp)
                self.player.basic_attack(target_enemy)
                print(target_enemy.hp)
                if target_enemy.hp[0] == 0:
                    self.board.handle_enemy_death(new_x, new_y)


    def draw_window(self):
        self.window.fill((0, 0, 0))
        self.load_game_board()
        self.load_player_panel()
        self.load_misc_panel()


    def load_game_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_LENGTH):
                pg.draw.rect(self.window, TILE_COLORS[self.board.template[y][x]],
                             (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        pg.draw.rect(self.window, colors.WHITE,
                     (TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT), 4)


    def load_player_panel(self):
        player_panel.draw_player_panel(self.window, self.player)

    def load_misc_panel(self):
        misc_panel.draw_misc_panel(self.window, self.board)

    def refresh_focus_window(self, focus_tile):
        misc_panel.draw_focus_window(self.window, self.board, focus_tile)
        pg.display.update()

    def game_loop_iteration(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return False
                # Check if input is for a basic movement, i.e. up, down, left, right
                elif event.key in self.player.movement_mapping.keys():
                    self.move_player_on_board(event.key)
                self.load_game_board()
                self.load_player_panel()

        return True