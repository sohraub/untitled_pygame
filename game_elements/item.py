
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = self.parse_description(description)

    def parse_description(self, full_string, char_limit=35):
        """
        A function to parse a description string into a list of strings that can fit into the item-
        display modal.
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


