import pygame as pg

from game_elements.board import Board
from game_elements.player import Player


class Game:
    def __init__(self, board=None, player=None, filename='untitlted'):
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
            print(self.board.template[old_y][old_x])
        else:
            self.player.x = old_x
            self.player.y = old_y
            print(self.board)


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