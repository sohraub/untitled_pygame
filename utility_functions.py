from config import TOP_LEFT_X, TOP_LEFT_Y, TILE_SIZE

"""
Module for storing little functions that could be useful throughout the project.
"""

def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def parse_description(full_string, char_limit=35):
    """
    A function to parse a description strings into a list of strings that can fit into tooltips.
    """
    parsed_string_list = list()
    temp_string = ''
    for word in full_string.split(' '):
        if len(temp_string + word) + 1 >= char_limit:
            parsed_string_list.append(temp_string)
            temp_string = ''
        temp_string += f'{word} '
    if 0 < len(temp_string) < char_limit:
        parsed_string_list.append(temp_string)
    return parsed_string_list


def check_adjacent(self, target):
    """Returns True if target is in an adjacent square to self, False otherwise."""
    if manhattan_distance((self.x, self.y), (target.x, target.y)) != 1:
        return False
    return True

def tile_from_xy_coords(x, y):
    """Given the xy-coordinates of an object on the game board, returns the pg.Rect dimensions of that object."""
    return (TOP_LEFT_X + (x * TILE_SIZE), TOP_LEFT_Y + (y * TILE_SIZE), TILE_SIZE, TILE_SIZE)

def xy_coords_from_tile(tile):
    """Given the pg.Rect dimensions of an object, returns the x,y coordinates of the object on the game board."""
    x = int((tile[0] - TOP_LEFT_X) / TILE_SIZE)
    y = int((tile[1] - TOP_LEFT_Y) / TILE_SIZE)
    return x, y
