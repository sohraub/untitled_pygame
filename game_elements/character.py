import random

from utility_functions import manhattan_distance


class Character:
    """
    Base class for Players and Enemies. Can perform all the basic actions such as moving and attacking.
    """
    def __init__(self, name, x=0, y=0, hp=None, mp=None, attributes=None, status=None):
        """
        Initialize a Character object. This is only ever called through super() for Player and Enemies.
        :param name: Name of the character
        :param x: Character's x-coordinate
        :param y: Character's y-coordinate
        :param hp: Character's HP represented as a list: [current, max]
        :param mp: Character's MP, represented same as hp.
        :param attributes: Dict containing the character's attributes.
        :param status: Dict containing a list of buffs and debuffs affecting this character
        """
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp if hp is not None else [5, 5]
        self.mp = mp if mp is not None else [5, 5]
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

    def move_to(self, destination):
        """Sets the characters position to 'destination'"""
        self.x = destination[0]
        self.y = destination[1]

    def move_up(self, steps=1):
        """Moves the character along the y-axis"""
        # Note that (0, 0) is the top left corner, so we subtract from  the y position to move up
        self.move_to((self.x, self.y - steps))

    def move_right(self, steps=1):
        """Moves the character along the x-axis"""
        self.move_to((self.x + steps, self.y))

    def apply_status(self, status):
        """
        Adds a new status, and applies attribute effects, if any. Also checks to see if player already has that status,
        and if so, just refreshes the turns left.
        """
        # We use self.status[f'{status.type}s'] to dynamically get the list of either buffs or debuffs, depending on
        # the type of status being applied.
        current_statuses = {x.name for x in self.status[f'{status.type}s']}
        if status.name in current_statuses:
            for x in self.status[f'{status.type}s']:
                if x.name == status.name:
                    # If player already has this status, reset the number of turns left to the duration of the newest
                    # instance of the status.
                    x.turns_left = status.duration
                    return
        self.status[f'{status.type}s'].append(status)
        if status.attribute_effects:
            for attribute in status.attribute_effects:
                self.attributes[attribute] += status.attribute_effects[attribute]

    def remove_status(self, status):
        """Removes an expired status, and removes attribute effects, if any."""
        self.status[f'{status.type}s'].remove(status)
        if status.attribute_effects:
            for attribute in status.attribute_effects:
                self.attributes[attribute] -= status.attribute_effects[attribute]

    def apply_end_of_turn_status_effects(self):
        """Applies effects of any end-of-turn statuses."""
        console_text = list()
        for status in self.status['buffs'] + self.status['debuffs']:
            if status.end_of_turn_effect:
                console_text.append(status.end_of_turn_effect(self))
            status.turns_left -= 1
            if status.turns_left == 0:
                self.remove_status(status)

        return console_text
