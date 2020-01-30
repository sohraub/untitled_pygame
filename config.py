import colors
"""
Config file to store most variables which have to do with main system stuff.
"""

####### DIMENSION VARIABLES #######
WINDOW_LENGTH = 1500
WINDOW_HEIGHT = 700

PLAY_LENGTH = 800
PLAY_HEIGHT = 500
TILE_SIZE = 50
TOP_LEFT_X = int((WINDOW_LENGTH - PLAY_LENGTH) / 2)
TOP_LEFT_Y = int((WINDOW_HEIGHT - PLAY_HEIGHT) / 2)
SIDE_PANEL_LENGTH = 300
SIDE_PANEL_HEIGHT = 600


###### TILE COLORS ######
TILE_COLORS = {
    'P': colors.GREEN,
    'E': colors.RED,
    'O': colors.GREY,
    'T': colors.GOLD,
    'D': colors.BROWN,
    'X': colors.BLACK
}


###### FONT FILES ######
SHADOWS_INTO_LIGHT = '.\\fonts\\ShadowsIntoLight.ttf'
