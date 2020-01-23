import pygame as pg

from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, \
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH
from game_elements.element_config_values import BOARD_HEIGHT, BOARD_LENGTH
from game_elements.board import Board
from game_elements.player import Player


class Game:
    def __init__(self, window, board=None, player=None, filename='untitlted'):
        self.window = window
        self.board = board
        self.player = player
        self.player.x = board.player_coordinates[0]
        self.player.y = board.player_coordinates[1]
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


    def draw_window(self):
        self.window.fill((0, 0, 0))
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_LENGTH):
                pg.draw.rect(self.window, TILE_COLORS[self.board.template[y][x]],
                             (TOP_LEFT_X + x * TILE_SIZE, TOP_LEFT_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
        pg.draw.rect(self.window, (255, 255, 255),
                     (TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT), 4)


    def draw_player_panel(self):
        panel_top_left_x = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2)
        panel_top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)
        pg.draw.rect(self.window, (255, 255, 255),
                     (panel_top_left_x, panel_top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)


    def draw_misc_panel(self):
        panel_top_left_x = WINDOW_LENGTH - ((TOP_LEFT_X - SIDE_PANEL_LENGTH) / 2) - SIDE_PANEL_LENGTH
        panel_top_left_y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) / 2)
        pg.draw.rect(self.window, (255, 255, 255),
                     (panel_top_left_x, panel_top_left_y, SIDE_PANEL_LENGTH, SIDE_PANEL_HEIGHT), 2)


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

        return True