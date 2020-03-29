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
