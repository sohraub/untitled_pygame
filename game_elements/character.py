class Character:
    def __init__(self, name, attributes=None, buffs=None, debuffs=None, move_speed=1):
        self.name = name
        self.x = 0
        self.y = 0
        self.attributes = attributes if attributes is not None else {'HP':5, 'MP':0}
        self.status = {
            'buffs': buffs if buffs is not None else list(),
            'debuffs': debuffs if debuffs is not None else list()
        }
        self.move_speed = move_speed