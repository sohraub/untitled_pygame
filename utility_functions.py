import copy
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

def find_min_steps(start, target, open_tiles):
    """
    Used primarily for enemy path-finding, this algorithm determines the next step for the character at 'position' to
    take if it wants to get to target. For enemy movement, this function is only called if the most obvious movements
    in pursuit of a target go through non-open tiles. For a detailed explanation, read the code along with comments.
    :param start: xy-coordinates of the start position
    :param target: xy-coordinates of the target
    :param open_tiles: list of xy-coordinates of open tiles in the board
    :return: min_steps, the minimum # of steps to reach the target
             next_step, the xy-coordinates of the next step along the minimum path
    """
    x, y = start
    # First build a list of the 4 tiles immediately adjacent to 'position'
    adjacent_tiles = ([(x + i, y) for i in [-1, 1]] + [(x, y + i) for i in [-1, 1]])
    # Then filter that list against the list of open tiles on the board
    adj_open_tiles = [tile for tile in adjacent_tiles if tile in set(open_tiles)]
    min_steps = 1000  # Initialize min_steps to a big number, in this case 1000
    next_step = (None, None)
    # First loop through every adj_open_tile to see if any are directly next to the target, in which case that will
    # be our next step
    for tile in adj_open_tiles:
        if manhattan_distance(tile, target) == 1:
            return 1, tile

    # If not, move on to going through each adj_open_tile and recursively finding the path with the smallest amount
    # of steps, and returning the next step along that path
    for tile in adj_open_tiles:
        new_open_tiles = copy.copy(open_tiles)
        # We remove the tile in question from open_tiles when recursively calling the function where position=tile, to
        # speed up the calculations since its unlikely that the ideal path involves that level of backtracking
        new_open_tiles.remove(tile)
        new_steps, new_tile = find_min_steps(tile, target, new_open_tiles)
        steps_to_target = 1 + new_steps
        # Once we've found the shortest path evolving from each of the adj_open_tiles, we return the number of steps
        # (to keep consistent with the recursive function call) and the actual coordinates of the next step.
        if steps_to_target < min_steps:
            min_steps = steps_to_target
            next_step = tile
    return min_steps, next_step

def get_knockback(self_x, self_y, target, knockback=1):
    """
    Determines the position of the target after direct knockback applied by self.
    :param self: The Character object knocking back target
    :param target: The Character object knocked back by self
    :param knockback: Number of tiles to be knocked back
    :return: (new_x, new_y) the position of target after the knockback
    """
    if self_x != target.x:
        new_x = target.x + knockback if self_x < target.x else target.x - knockback
        new_y = target.y
    else:
        new_y = target.y + knockback if self_y < target.y else target.y - knockback
        new_x = target.x
    return new_x, new_y
