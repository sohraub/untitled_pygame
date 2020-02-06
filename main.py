import pygame as pg


from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE,\
    TILE_COLORS, SIDE_PANEL_HEIGHT, SIDE_PANEL_LENGTH
from game import Game
from game_elements.board import Board
from game_elements.board_templates import TEMPLATES
from game_elements.player import Player, load_player_from_json



def load_board():
    template = TEMPLATES[0]
    board = Board(template)
    return board


def main_menu(window):
    main(window)


def handle_user_input():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                return False

    return True


def main(window):
    game = Game(window, player=load_player_from_json(".\\saves\\first.json"), board=Board(tier=1))
    run = True
    game.draw_window()
    while run:
        # game_loop_iteration() returns a boolean based on whether or not the game should keep running
        run = game.game_loop_iteration()
        pg.display.update()


if __name__ == '__main__':
    pg.font.init()
    window = pg.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
    pg.display.set_caption('Untitled Game # 1')
    main_menu(window)