from game_elements.character import Character


class Player(Character):
    def __init__(self, name, x=0, y=0, attributes=None, buffs=None, debuffs=None, move_speed=1, in_combat=False,
                 inventory=None, equipment=None):
        super().__init__(name, x, y, attributes, buffs, debuffs, move_speed, in_combat)
        self.inventory = inventory if inventory is not None else dict()
        self.equipment = equipment if equipment is not None else {
            'head': None,
            'body': None,
            'weapon': None,
            'hands': None,
            'feet': None
        }
