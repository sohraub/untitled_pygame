import pygame as pg


from config import WINDOW_HEIGHT, WINDOW_LENGTH, TOP_LEFT_Y, TOP_LEFT_X, PLAY_HEIGHT, PLAY_LENGTH, TILE_SIZE, COLORS
from game import Game
from game_elements.board import Board
from game_elements.board_templates import TEMPLATES
from game_elements.element_config_values import BOARD_HEIGHT, BOARD_LENGTH
from game_elements.player import Player, load_player_from_json


def draw_window(window, board):
    window.fill((0, 0, 0))
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            pg.draw.rect(window, COLORS[board.template[y][x]],
                         (TOP_LEFT_X + x*TILE_SIZE, TOP_LEFT_Y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
    pg.draw.rect(window, (255, 255, 255),
                 (TOP_LEFT_X, TOP_LEFT_Y, PLAY_LENGTH, PLAY_HEIGHT), 4)


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
    game = Game(board=load_board(), player=load_player_from_json(".\\saves\\first.json"))
    draw_window(window, game.board)
    run = True
    while run:
        # game_loop_iteration() returns a boolean based on whether or not the game should keep running
        run = game.game_loop_iteration()
        draw_window(window, game.board)
        pg.display.update()




if __name__ == '__main__':
    pg.font.init()
    window = pg.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))
    pg.display.set_caption('Untitled Game # 1')
    main_menu(window)