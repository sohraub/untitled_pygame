import colors
import os
"""
Config file to store most variables which have to do with main system stuff.
"""

####### DIMENSION VARIABLES #######
WINDOW_LENGTH = 1500
WINDOW_HEIGHT = 750

PLAY_LENGTH = int(WINDOW_LENGTH * 0.4)  # Currently: 600
PLAY_HEIGHT = int(WINDOW_HEIGHT * 0.8)  # Currently: 600
TILE_SIZE = int(PLAY_LENGTH / 15)  # Currently: 40
TOP_LEFT_X = int((WINDOW_LENGTH - PLAY_LENGTH) / 2)  # Currently: 450
TOP_LEFT_Y = int((WINDOW_HEIGHT - PLAY_HEIGHT) / 2 + int(WINDOW_HEIGHT / 15))  # Currently: 125
SIDE_PANEL_LENGTH = int(WINDOW_LENGTH * 0.25)  # Currently: 375
SIDE_PANEL_HEIGHT = int(WINDOW_HEIGHT * 0.98)  # Currently: 735

PLAYER_PANEL_TOP_LEFT_X = int((TOP_LEFT_X - SIDE_PANEL_LENGTH) * 0.5)  # Currently: 38
PLAYER_PANEL_TOP_LEFT_Y = int((WINDOW_HEIGHT - SIDE_PANEL_HEIGHT) * 0.5)  # Currently: 8

###### TILE COLORS ######
TILE_COLORS = {  # Mapping of letters to tile type is as follows:
    'P': colors.GREEN,  # Player
    'E': colors.RED,  # Enemies
    'O': colors.GREY,  # Open tiles
    'T': colors.GOLD,  # Treasure chests
    'D': colors.BROWN,  # Doors
    'X': colors.BLACK,  # Walls/out-of-play tiles
    'R': colors.DARK_GREEN  # Traps
}


###### FONT FILES ######
font_SIL = os.path.join('fonts', 'ShadowsIntoLight.ttf')

