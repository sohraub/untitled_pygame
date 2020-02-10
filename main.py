import pygame as pg

from rendering import window_renderer

from game import Game
from console import Console
from game_elements.board import Board
from game_elements.board_templates import TEMPLATES
from game_elements.player import Player, load_player_from_json


def load_board():
    template = TEMPLATES[0]
    board = Board(template)
    return board


def main_menu(window):
    main_game(window)


def handle_user_input():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                return False

    return True


def main_game():
    game = Game(console=Console(), player=load_player_from_json(".\\saves\\first.json"), board=Board(tier=1))
    run = True
    game.draw_window()
    game.console.refresh_console()
    while run:
        # game_loop_iteration() returns a boolean based on whether or not the game should keep running
        run = game.game_loop_iteration()
        pg.display.update()


if __name__ == '__main__':
    main_menu()