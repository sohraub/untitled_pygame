from utility_functions import parse_description

class Item:
    def __init__(self, name, description):
        """
        General class for items, which can be either Consumable or Equipment.
        :param name: Name of the item.
        :param description: Description to be displayed on the item-display modal.
        """
        self.name = name
        self.description = parse_description(description, char_limit=33)

    def is_consumable(self):
        return self.__class__.__name__ == 'Consumable'

    def is_equipment(self):
        return self.__class__.__name__ == 'Equipment'


class Consumable(Item):
    def __init__(self, name, description, effects, parameters=None, details=None, console_text='', prereqs=None):
        """
        Specific extended class of items that can be consumed. For info on parameters used in super(), refer to the
        Item docstring.
        :param effects: The function(s) a consumable calls when used.
        :param parameters: List of dict representations of the parameters used in the effect functions.
        :param details: List of effects to display in the item window.
        :param console_text: Text that will be printed to console when you consume the item.
        :param prereqs: Some items have certain pre-requisites that need to be met before they can be used. These will
                        be checked by the Game object before an item can be used.
        """
        super().__init__(name, description)
        self.effects = effects
        self.parameters = parameters if parameters is not None else [dict()]
        self.details = details if details is not None else list()
        self.console_text = console_text
        self.prerequisites_for_use = prereqs

    def to_dict(self):
        """Returns a dict representation of the object, to be used in rendering modules."""
        return {
            'type': 'consumable',
            'name': self.name,
            'description': self.description,
            'details': self.details
        }


class Equipment(Item):
    def __init__(self, name, description, slot, off_rating=0, def_rating=0, bonuses=None, rarity=0, stat_req=None) :
        """
        Subclass of Item for items that can be equipped to the character.

        :param slot: Where this can be equipped, e.g. 'head', 'body', etc.
        :param off_rating: An int, the bonus to offense given by equipping this item.
        :param def_rating: An int, the bonus to defense given by equipping this item.
        :param bonuses: A dict of functions and parameters, for any extra bonuses this item gives.
        :param rarity: An int, which determines the kind of bonuses this item can have.
        :param stat_req: A dict which has the minimum stats required to equip this item. If None, then this item has
                         no stat requirements.
        """
        super().__init__(name, description)
        self.slot = slot
        self.off_rating = off_rating
        self.def_rating = def_rating
        self.bonuses = bonuses
        self.rarity = rarity
        self.stat_req = stat_req

    def to_dict(self):
        """Returns a dict representation of the object, to be used in rendering modules."""
        return {
            'type': 'equipment',
            'name': self.name,
            'description': self.description,
            'slot': self.slot,
            'off_rating': self.off_rating,
            'def_rating': self.def_rating,
            'bonuses': self.bonuses,
            'rarity': self.rarity,
            'stat_req': self.stat_req
        }
