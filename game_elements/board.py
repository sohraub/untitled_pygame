import random
from uuid import uuid4
from time import sleep

from game_elements import enemy
from game_elements import trap
from game_elements import chest
from game_elements.element_config_values import BOARD_LENGTH, BOARD_HEIGHT



def choose_random_board():
    """Function which just returns a random board template from the board_templates.py module."""
    import random
    from element_lists.board_templates import TEMPLATES
    return random.choice(TEMPLATES)


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
    def __init__(self, board_template=None, tier=1):
        """
        The Board object will be responsible for holding all of the data which is specific to each board and
        nothing else.

        :param board_template: The template the board is loaded from.
        :param tier: The tier of the board, which is used to determine the levels of enemies and items generated.

        In this init function, the following attributes are also set based on the board template:
        :player_coordinates: The (x, y) position of the player on the board
        :enemies: A dict containing all of the enemies on the board, in the format (x, y): Enemy()
        :chests: A dict containing all of the chests on the board, in the format (x, y): Chest()
        :tile_mapping: A dict that contains entries for each tile type, the value of which is a list of all the
                       coordinates of tiles of that type.
        """
        self.template = board_template if board_template is not None else choose_random_board()
        self.tier = tier
        self.player_coordinates = None
        self.enemies = dict()
        self.chests = dict()
        self.traps = dict()
        self.tile_mapping = {
            # Each letter corresponds to:
            'X': list(),  # Wall tiles
            'D': list(),  # Doors
            'T': list(),  # Treasure
            'O': list(),  # Open tiles
            'R': list(),  # Traps
            'E': list()   # Enemies
        }
        for y in range(len(self.template)):
            for x in range(len(self.template[y])):
                if self.template[y][x] == 'P':
                    self.player_coordinates = (x, y)
                elif self.template[y][x] in self.tile_mapping.keys():
                    self.tile_mapping[self.template[y][x]].append((x, y))
        self.enemies = dict()
        for coord in self.tile_mapping['E']:
            self.enemies[coord] = enemy.generate_new_enemy(x=coord[0], y=coord[1], tier=self.tier)
        for coord in self.tile_mapping['T']:
            self.chests[coord] = chest.generate_chest(tier=self.tier)
        for coord in self.tile_mapping['R']:
            self.traps[coord] = trap.generate_random_trap(coord)

    def rebuild_template(self):
        """
        This method rebuilds the board template based off of the tile_mapping dict. It will be called every time the
        position of an object on the board changes, so that the board can be re-rendered based off of the new template.
        """
        new_template = [['O' for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)]
        for tile_type in self.tile_mapping.keys():
            for coord in self.tile_mapping[tile_type]:
                new_template[coord[1]][coord[0]] = tile_type

        new_template[self.player_coordinates[1]][self.player_coordinates[0]] = 'P'
        self.template = new_template

    def tile_is_open(self, x, y):
        """Method that simply returns a boolean signifying if the passed in coordinate is of an open tile."""
        if (x, y) in set(self.tile_mapping['O'] + self.tile_mapping['R']):
            return True
        return False

    def handle_enemy_death(self, enemy_pos):
        """Method called when an enemy dies, removing it from the tile_mapping and rebuilding the template."""
        del self.enemies[enemy_pos]
        self.tile_mapping['E'].remove(enemy_pos)
        self.tile_mapping['O'].append(enemy_pos)
        self.rebuild_template()

    def update_enemy_position(self, old_pos, new_pos):
        """
        Method called when an enemy has moved, updating it's entry in the enemies and tile_mapping dicts and
        rebuilding the template
        """
        # We only update the tile mapping if the enemy moves to an open space, since if they're moving to a trap, we
        # still want the tile to stay in the list of trap tiles.
        if new_pos in set(self.tile_mapping['O']):
            self.tile_mapping['O'].remove(new_pos)
        self.tile_mapping['O'].append(old_pos)
        self.enemies[new_pos] = self.enemies.pop(old_pos)  # Updates the key-value pair of the actual Enemy object
        self.enemies[new_pos].x = new_pos[0]  # Updates the Enemy object's coordinate values
        self.enemies[new_pos].y = new_pos[1]
        self.tile_mapping['E'].remove(old_pos)
        self.tile_mapping['E'].append(new_pos)
        self.rebuild_template()

    def update_player_position(self, old_pos, new_pos):
        """
        Updates the position values in the Board class to reflect player movement, i.e. updating the player_coordinate
        values and adding the old position to the set of open tiles.
        """
        if new_pos in set(self.tile_mapping['O']):  # Don't want to remove coordinates if the player steps on a trap
            self.tile_mapping['O'].remove(new_pos)
        self.tile_mapping['O'].append(old_pos)
        self.player_coordinates = new_pos

    def handle_chest_has_been_opened(self, chest_pos):
        """Method called when a chest has been opened, modifying the chest in the chests dict."""
        chest = self.chests[chest_pos]
        chest.opened = True
        # TODO: Add some kind of rendering logic to make open chests look different

    def handle_trap_triggered(self, trap_pos):
        """Removes trap from board if triggered."""
        del self.traps[trap_pos]
        self.tile_mapping['R'].remove(trap_pos)
        self.tile_mapping['O'].append(trap_pos)

    def move_character(self, character, new_x, new_y):
        console_text = list()
        if self.template[new_y][new_x] == 'R':  # Moving to a tile with a trap
            console_text.append(self.handle_step_on_trap((new_x, new_y), character))
        if character.__class__.__name__ == 'Player':
            self.update_player_position(old_pos=(character.x, character.y), new_pos=(new_x, new_y))
        elif character.__class__.__name__ == 'Enemy':
            self.update_enemy_position(old_pos=(character.x, character.y), new_pos=(new_x, new_y))
        character.x, character.y = new_x, new_y
        self.rebuild_template()

        return console_text

    def handle_step_on_trap(self, trap_pos, target):
        """
        Check to see if trap is triggered, and if so, applies the trap effect and handles removing the trap from
        the board
        :param trap_pos: Coordinates of the trap
        :param target: The Character which triggered the trap.
        :returns: New lines for console.
        """
        enemy_target = True if target.__class__.__name__ == 'Enemy' else False
        trap = self.traps[trap_pos]
        if enemy_target:
            console_text = f'The {target.display_name} steps on a {trap.name} trap, '
            # console_text.append(f'The {target.display_name} steps on a {trap.name} trap, ')
        else:
            console_text = f'You step on a {trap.name} trap, '
            # console_text.append(f'You step on a {trap.name} trap, ')
        avoid_probability = 100 * (1 - trap.trigger_prob) + (trap.trigger_avoid_coeff * target.attributes["dex"])
        if random.randint(0, 100) > avoid_probability:
            if trap.type == 'direct':
                damage = trap.function(target)
                target.hp[0] = max(0, target.hp[0] - damage)
                console_text += f'taking {damage} damage.'
            elif trap.type == 'debuff':
                effect = trap.function(target)
                console_text += f'and become{"s" if enemy_target else ""} {effect}.'
            self.handle_trap_triggered(trap_pos)

        else:
            console_text += f'but avoid{"s" if enemy_target else ""} triggering it.'

        return console_text