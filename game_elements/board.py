from game_elements.element_config_values import BOARD_LENGTH, BOARD_HEIGHT


class Board:
    """
    Class representing the game's board object. These will be initialized from a list of strings called the
    board_template, e.g.
    board_template = ['XXXXXXXXXXXXDXXX',
                      'XOOEOTOOOOOOOOOX',
                      'XOOOOOOOOOOEOOOX',
                      'XOOOOOEOOOOOOOOX',
                      'XXXXXXOOOOXXXXXX',
                      'XXXXXXOOOOXXXXXX',
                      'XXXXXXOOOOXXXXXX',
                      'XXXXOOOOOOOOXXXX',
                      'XXXXOOOOPOOOXXXX',
                      'XXXXXXXXDXXXXXXX']
    according to the tile_mapping below.
    """
    def __init__(self, board_template):
        self.template = board_template
        self.tile_mapping = {
            # Each letter corresponds to:
            'X': list(),  # Blank tiles
            'E': list(),  # Enemies
            'D': list(),  # Doors
            'T': list(),  # Treasure
            'O': list()   # Open tiles
        }
        for y in range(len(self.template)):
            for x in range(len(self.template[y])):
                if self.template[y][x] == 'P':
                    self.player_coordinates = (x, y)
                elif self.template[y][x] in self.tile_mapping.keys():
                    self.tile_mapping[self.template[y][x]].append((x, y))

    def __str__(self):
        board = ''
        for y in range(len(self.template)):
            for x in range(len(self.template[y])):
               board += '{} '.format(self.template[y][x])
            board += '\n'
        return board

    def rebuild_template(self):
        new_template = [['O' for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)]
        for tile_type in self.tile_mapping.keys():
            for coord in self.tile_mapping[tile_type]:
                new_template[coord[1]][coord[0]] = tile_type

        new_template[self.player_coordinates[1]][self.player_coordinates[0]] = 'P'
        print(self.player_coordinates)
        for x in new_template:
            print(x)
        self.template = new_template

    def tile_is_open(self, x, y):
        if (x, y) in set(self.tile_mapping['O']):
            return True
        return False



