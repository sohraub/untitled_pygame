"""
Config file to store most variables which have to do with main system stuff.
"""

####### DIMENSION VARIABLES #######
WINDOW_LENGTH = 1200
WINDOW_HEIGHT = 700

PLAY_LENGTH = 800
PLAY_HEIGHT = 500
TILE_SIZE = 50
TOP_LEFT_X = int((WINDOW_LENGTH - PLAY_LENGTH) / 2)
TOP_LEFT_Y = int((WINDOW_HEIGHT - PLAY_HEIGHT) / 2)


###### COLORS ######
COLORS = {
    'P': (102, 204, 0),
    'E': (255, 51, 51),
    'O': (173, 173, 173),
    'T': (153, 153, 0),
    'D': (153, 102, 51),
    'X': (0, 0, 0)
}
