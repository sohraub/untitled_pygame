
class Item:
    def __init__(self, name, description):
        """
        General class for items, which can be either Consumable or Equipment.
        :param name: Name of the item.
        :param description: Description to be displayed on the item-display modal.
        """
        self.name = name
        self.description = self.parse_description(description)

    def parse_description(self, full_string, char_limit=35):
        """
        A function to parse a description string into a list of strings that can fit into the item-display modal.
        """
        parsed_string_list = list()
        temp_string = ''
        for word in full_string.split(' '):
            if len(temp_string + word) + 1 >= char_limit:
                parsed_string_list.append(temp_string)
                temp_string = ''
            temp_string += f'{word} '
        if 0 < len(temp_string) < char_limit:
            parsed_string_list.append(temp_string)
        return parsed_string_list


class Consumable(Item):
    def __init__(self, name, description, effects, parameters, details=None, verb='used'):
        """
        Specific extended class of items that can be consumed. For info on parameters used in super(), refer to the
        Item docstring.
        :param effects: The function(s) a consumable calls when used.
        :param parameters: List of dict representations of the parameters used in the effect functions.
        :param details: List of effects to display in the item window.
        :param verb: Verb that will be printed to console when the player uses this item.
        """
        super().__init__(name, description)
        self.effects = effects
        self.parameters = parameters
        self.details = details if details is not None else list()
        self.verb = verb

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
