
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Consumable(Item):
    def __init__(self, name, description, effects, parameters, details=None):
        super().__init__(name, description)
        self.effects = effects
        self.parameters = parameters
        self.details = details if details is not None else list()

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'details': self.details
        }


