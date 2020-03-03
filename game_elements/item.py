
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
            'name': self.name,
            'description': self.description,
            'details': self.details
        }


