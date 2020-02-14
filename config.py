import colors
"""
Config file to store most variables which have to do with main system stuff.
"""

####### DIMENSION VARIABLES #######
WINDOW_LENGTH = 1200
WINDOW_HEIGHT = 750

#TODO: Change these values to be percentages of the above values only
PLAY_LENGTH = int(WINDOW_LENGTH * 0.5)
PLAY_HEIGHT = int(WINDOW_HEIGHT * 0.8)
TILE_SIZE = int(PLAY_LENGTH / 15)
TOP_LEFT_X = int((WINDOW_LENGTH - PLAY_LENGTH) / 2)
TOP_LEFT_Y = int((WINDOW_HEIGHT - PLAY_HEIGHT) / 2)
SIDE_PANEL_LENGTH = int(WINDOW_LENGTH * 0.2)
SIDE_PANEL_HEIGHT = int(WINDOW_HEIGHT * 0.98)


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
