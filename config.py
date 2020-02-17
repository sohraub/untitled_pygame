import colors
"""
Config file to store most variables which have to do with main system stuff.
"""

####### DIMENSION VARIABLES #######
WINDOW_LENGTH = 1500
WINDOW_HEIGHT = 750

PLAY_LENGTH = int(WINDOW_LENGTH * 0.4)
PLAY_HEIGHT = int(WINDOW_HEIGHT * 0.8)
TILE_SIZE = int(PLAY_LENGTH / 15)
TOP_LEFT_X = int((WINDOW_LENGTH - PLAY_LENGTH) / 2)
TOP_LEFT_Y = int((WINDOW_HEIGHT - PLAY_HEIGHT) / 2 + int(WINDOW_HEIGHT / 15))
SIDE_PANEL_LENGTH = int(WINDOW_LENGTH * 0.25)
SIDE_PANEL_HEIGHT = int(WINDOW_HEIGHT * 0.98)


######## GAME ELEMENT VARIABLES ########
BOARD_LENGTH = 15
BOARD_HEIGHT = 15


###### TILE COLORS ######
"""
Mapping of letters to tile type is as follows:
    P - Player
    E - Enemy
    O - Open tile
    T - Treasure chest
    D - Door
    X - Out-of-play tile
"""
TILE_COLORS = {
    'P': colors.GREEN,
    'E': colors.RED,
    'O': colors.GREY,
    'T': colors.GOLD,
    'D': colors.BROWN,
    'X': colors.BLACK
}


###### FONT FILES ######
font_SIL = '.\\fonts\\ShadowsIntoLight.ttf'
