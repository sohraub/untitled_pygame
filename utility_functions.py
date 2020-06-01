import copy
from heapq import heapify, heappush, heappop

from config import TOP_LEFT_X, TOP_LEFT_Y, TILE_SIZE
from game_elements.element_config_values import BOARD_HEIGHT, BOARD_LENGTH

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


def reconstruct_path(came_from, current):
    """
    Called by find_best_step() below when an optimal path has been found, to retrace the steps taken to get to that path
    and return the first step along that path.
    :param came_from: A dict that will be in the format
                        {(x, y): coordinate immediately proceeding (x, y)}
                      for each step which was explored throughout find_best_step()
    :param current: The current step being looked at. Will be initialized the position of goal, and steps will be traced
                    backwards along came_from.
    :return: The second-last element of the 'path'. This list will hold every step going backwards from the goal, so
             that path[0] is the goal and path[-1] is the start, hence we return path[-2] to be the next step.
    """
    path = [current]
    while current in set(came_from.keys()):
        current_temp = came_from[current]
        del came_from[current]
        current = current_temp
        path.append(current)

    return path[-2]


def find_best_step(start, goal, open_tiles):
    """
    An implementation of the A* search algorithm to find the best next step for a character at start trying to get to
    goal. Additional details will be provided in in-line comments.
    For more info check out https://en.wikipedia.org/wiki/A*_search_algorithm
    :param start: (x,y)-coordinates of the character's starting position
    :param goal: (x,y)-coordinates of the goal position
    :param open_tiles: A list of the coordinates of every open tile on the board
    :return: (x,y) coordinates of the best next step, or None, None if no path was found.
    """
    # We add 'goal' to the list of open tiles because this algorithm will terminate when it steps to goal, so it needs
    # to be available as an option.
    open_tiles.append(goal)
    # g_scores will be the manhattan_distance from the start to each tile. Initialize every value to 1000
    g_scores = {tile: 1000 for tile in open_tiles}
    g_scores[start] = 0
    # f_scores will be, for each tile, the g_score of that tile + manhattan_distance(tile, goal), i.e. an estimate
    # of the number of steps to reach the goal going through this tile.
    f_scores = {tile: 1000 for tile in open_tiles}
    f_scores[start] = manhattan_distance(start, goal)
    # came_from will be a dict where each key is a tile and the value is the tile immediately proceeding it on our path
    came_from = {}
    # open_set will be a min-heap of each tile, sorted by their f_scores. Stored as a tuple of (f_score, (x, y))
    open_set = []
    heapify(open_set)
    heappush(open_set, (f_scores[start], start))
    while open_set:
        # current will always be set to the tile in open_set with the smallest f_score
        current = open_set[0][1]
        if current == goal:
            # If we reach here, then we're done
            return reconstruct_path(came_from, current)

        heappop(open_set)
        # Build a list of every neighbour of current
        adjacent_tiles = ([(current[0] + i, current[1]) for i in [-1, 1]] + [(current[0], current[1] + i)
                                                                             for i in [-1, 1]])
        adj_open_tiles = [tile for tile in adjacent_tiles if tile in set(open_tiles)]
        for neighbour in adj_open_tiles:
            temp_g_score = g_scores[current] + manhattan_distance(current, neighbour)
            # If temp_g_score is lower than what we have stored, then we've found a shorter path through neighbour
            # than we had previously.
            if temp_g_score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = temp_g_score
                f_scores[neighbour] = g_scores[neighbour] + manhattan_distance(neighbour, goal)
                if (neighbour, f_scores[neighbour]) not in open_set:
                    heappush(open_set, (f_scores[neighbour], neighbour))

    return None, None


def find_tiles_in_radius(center_x, center_y, radius, **kwargs):
    """Returns a list of every tile that has a manhattan distance of <= radius around the tile (center_x, center_y)"""
    tiles_in_radius = [(center_x + i, center_y + j)
                       for i in range(-(radius + 1), radius + 1)
                       for j in range(-(radius + 1), radius + 1)
                       if (abs(i) + abs(j) <= radius) and
                          (0 < (center_x + i) < BOARD_LENGTH and 0 < (center_y + j) < BOARD_HEIGHT)]
    tiles_in_radius.remove((center_x, center_y))
    return tiles_in_radius


def find_tiles_in_radius_of_1(center_x, center_y, **kwargs):
    """Calls find_tiles_in_radius() with a radius of 1"""
    return find_tiles_in_radius(center_x, center_y, radius=1)


def find_tiles_in_line_from_player_to_end(target_x, target_y, player_x, player_y):
    """
    Returns a list of every tile in a line from the player's coordinates to the end of the board, going through the
    target coordinates.
    """
    if target_x == player_x:  # Then we're moving in a vertical direction:
        iter_range = range(0, player_y) if target_y < player_y else range(player_y + 1, BOARD_HEIGHT)
        return [(player_x, i) for i in iter_range if i != target_y]  # The condition here is to avoid counting the
                                                                     # targeted enemy twice.
    else:  # Then we're moving in a horizontal direction:
        iter_range = range(0, player_x) if target_x < player_x else range(player_x + 1, BOARD_LENGTH)
        return [(i, player_y) for i in iter_range if i != target_x]


def find_exit_direction(board_template, door_x, door_y):
    max = BOARD_HEIGHT - 1
    if door_x == 0:
        return 'left'
    if door_x == max:
        return 'right'
    if door_y == 0:
        return 'top'
    if door_y == max:
        return 'bottom'
    # If the door is not on one of the edges, then check the tiles immediately before and after it in each direction
    if board_template[door_y][door_x + 1] != 'X' and board_template[door_y][door_x - 1] == 'X':
        return 'left'
    if board_template[door_y][door_x - 1] != 'X' and board_template[door_y][door_x + 1] == 'X':
        return 'right'
    if board_template[door_y + 1][door_x] != 'X' and board_template[door_y - 1][door_x] == 'X':
        return 'top'
    if board_template[door_y - 1][door_x] != 'X' and board_template[door_y + 1][door_x] == 'X':
        return 'bottom'


def find_appropriate_entrance(board_template, target_direction):
    door_coordinates = list()
    for i in range(len(board_template)):
        for j in range(len(board_template[i])):
            if board_template[i][j] == 'D':
                door_coordinates.append((j, i))
    for door_coord in door_coordinates:
        if find_exit_direction(board_template, door_coord[0], door_coord[1]) == target_direction:
            return (door_coord[0], door_coord[1])
    return None


def rotate_board(board_template):
    new_template = copy.copy(board_template)
    for i in range(len(new_template)):
        new_template[i] = ''.join(board_template[x][i] for x in range(len(new_template)))
    return new_template
