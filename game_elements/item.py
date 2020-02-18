
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Consumable(Item):
    def __init__(self, name, description, effects, parameters):
        super().__init__(name, description)
        self.effects = effects
        self.parameters = parameters


