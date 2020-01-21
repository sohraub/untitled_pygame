from utility_functions import get_manhattan_distance


class Character:
    def __init__(self, name, attributes=None, buffs=None, debuffs=None, move_speed=1, in_combat=False):
        self.name = name
        self.x = 0
        self.y = 0
        self.attributes = attributes if attributes is not None else {'HP':5, 'MP':0}
        self.status = {
            'buffs': buffs if buffs is not None else list(),
            'debuffs': debuffs if debuffs is not None else list()
        }
        self.move_speed = move_speed
        self.in_combat = in_combat

    def move_to(self, destination):
        if self.in_combat:
            if get_manhattan_distance((self.x, self.y), destination) > self.move_speed:
                return False
        self.x = destination[0]
        self.y = destination[1]