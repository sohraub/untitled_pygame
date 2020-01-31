from utility_functions import get_manhattan_distance


class Character:
    def __init__(self, name, x=0, y=0, attributes=None, status=None, move_speed=1, in_combat=False):
        self.name = name
        self.x = x
        self.y = y
        self.attributes = attributes if attributes is not None else {
            "str": 2,
            "dex": 2,
            "int": 2,
            "end": 2,
            "vit": 2,
            "wis": 2
        }
        self.status = status if status is not None else {
            'buffs': list(),
            'debuffs': list()
        }
        self.move_speed = move_speed
        self.in_combat = in_combat

    def move_to(self, destination):
        if self.in_combat:
            if get_manhattan_distance((self.x, self.y), destination) > self.move_speed:
                return False
        self.x = destination[0]
        self.y = destination[1]

    def move_up(self, steps=1):
        # Note that (0, 0) is the top left corner, so we subtract from
        # the y position to move up
        self.move_to((self.x, self.y - steps))

    def move_right(self, steps=1):
        self.move_to((self.x + steps, self.y))