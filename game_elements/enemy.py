from game_elements.character import Character
from utility_functions import get_manhattan_distance


class Enemy(Character):
    def __init__(self, name, x=0, y=0, attributes=None, buffs=None, debuffs=None, move_speed=1, in_combat=False,
                 aggro_range=3):
       super().__init__(name, x, y, attributes, buffs, debuffs, move_speed, in_combat)
       self.aggro_range = aggro_range

    def check_aggro(self, player):
        if get_manhattan_distance((self.x, self.y), (player.x, player.y)) <= self.aggro_range:
            self.in_combat = True
            player.in_combat = True
            return True
        return False
