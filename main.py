import pygame as pg

from game import Game
from console import Console
from game_elements.board import Board
from game_elements.player import Player


"""
Main module of the game, which kicks things off by calling the main_menu() method.
"""


def main_menu():
    """Loads the main menu screen, from which players can (eventually) navigate to the main game or other parts."""
    main_game()


def main_game():
    """Loads the main game."""
    game = Game(console=Console(), player=Player())
    run = True
    game.draw_window()
    game.console.refresh_console()
    while run:
        # game_loop_iteration() returns a boolean based on whether or not the game should keep running
        run = game.game_loop_iteration()
        pg.display.update()


if __name__ == '__main__':
    main_menu()
