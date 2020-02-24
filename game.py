import pygame as pg
from time import sleep

import colors

from utility_functions import manhattan_distance
from rendering import window_renderer, board_renderer
from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH, font_SIL
from game_elements.element_config_values import BOARD_HEIGHT, BOARD_LENGTH
from game_elements.board import Board
from game_elements.player import Player
from misc_panel import MiscPanel
from player_panel import PlayerPanel


class Game:
    def __init__(self, console, board=None, player=None, filename='untitlted'):
        self.console = console
        self.board = board if board is not None else Board()
        self.player = player if player is not None else Player()
        self.player.x = self.board.player_coordinates[0]
        self.player.y = self.board.player_coordinates[1]
        self.filename = filename
        self.player_panel = None
        self.misc_panel = None


    def move_player_on_board(self, input):
        """
        Given a basic movement input, moves the player character and updates its position
        on the board
        """
        console_text = list()
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
                # The handle_attacking_enemy function returns a text string to be displayed in the console
                console_text.append(self.handle_attacking_enemy((new_x, new_y)))
            if self.board.template[new_y][new_x] == 'T':  # Moving a tile which contains a chest opens the chest
                console_text.append(self.handle_opening_chest((new_x, new_y)))

        if console_text:
            self.console.update_console(console_text)


    def handle_opening_chest(self, chest_pos):
        target_chest = self.board.chests[chest_pos]
        if target_chest.opened:
            return 'This chest is empty. '
        # pick_up_item returns text for the console as well as a boolean signifying the success of picking up item
        console_text, success = self.player.pick_up_item(target_chest.item)
        if success:
            self.board.handle_chest_has_been_opened(chest_pos)
            self.player_panel.refresh_inventory()
        return console_text


    def handle_attacking_enemy(self, enemy_pos):
        self.refresh_focus_window(enemy_pos)
        target_enemy = self.board.enemies[enemy_pos]
        battle_text = self.player.basic_attack(target_enemy)
        if target_enemy.hp[0] == 0:
            self.board.handle_enemy_death(enemy_pos)
            self.misc_panel.focus_tile = None
            self.refresh_focus_window()
        return battle_text


    def start_enemy_turn(self):
        enemies = list()
        for enemy_coord in self.board.enemies:
            enemies.append(self.board.enemies[enemy_coord])
        for enemy in enemies:
            console_text = list()
            distance_to_player = manhattan_distance((enemy.x, enemy.y), (self.player.x, self.player.y))
            if distance_to_player <= enemy.attack_range:
                console_text.append(enemy.basic_attack(self.player, enemy_attack=True))
            elif distance_to_player <= enemy.aggro_range:
                new_position = enemy.move_towards_target((self.player.x, self.player.y), self.board.tile_mapping['O'])
                if new_position is not None:
                    self.board.update_enemy_position((enemy.x, enemy.y), new_position)
                    enemy.x = new_position[0]
                    enemy.y = new_position[1]
                    self.load_game_board()

            if console_text:
                self.console.update_console(console_text)


    def handle_turn_end(self):
        # These functions each return a boolean which determines whether any of the info has changes, and thus needs
        # re-drawing
        if self.player.conditions_worsen():
            self.player_panel.refresh_hp_mp()
            self.player_panel.refresh_conditions()
            self.player_panel.refresh_attributes()
        if self.player.check_fatigue():
            self.player_panel.refresh_attributes()

    def draw_window(self):
        self.load_game_board()
        self.load_player_panel()
        self.load_misc_panel()

    def load_game_board(self):
        board_renderer.render_game_board(self.board.template)

    def load_player_panel(self):
        self.player_panel = PlayerPanel(self.player)

    def load_misc_panel(self):
        self.misc_panel = MiscPanel(self.board)

    def refresh_focus_window(self, focus_tile=None):
        self.misc_panel.refresh_focus_window(focus_tile)

    def game_loop_iteration(self):
        for event in pg.event.get():
            if self.player_panel.panel_rect.collidepoint(pg.mouse.get_pos()):
                self.player_panel.handle_panel_mouseover()
                if self.player_panel.item_window_active is not None and\
                    not self.player_panel.item_window_active.collidepoint(pg.mouse.get_pos()):
                    self.player_panel.refresh_inventory()
                    self.player_panel.item_window_active = None
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return False
                elif event.type == pg.K_SPACE:
                    self.player.wait()
                # Check if input is for a basic movement, i.e. up, down, left, right
                elif event.key in self.player.movement_mapping.keys():
                    self.move_player_on_board(event.key)
                self.start_enemy_turn()
                self.handle_turn_end()
                self.player_panel.refresh_hp_mp()
                self.load_game_board()

        return True
