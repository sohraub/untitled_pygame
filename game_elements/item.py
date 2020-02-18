
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Consumable(Item):
    def __init__(self, name, description, effects):
        super().__init__(name, description)
        self.effects = effects


def increase_hp(target, value):
    target.hp += value

def improve_condition(target, condition, value):

