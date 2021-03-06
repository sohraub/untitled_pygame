import random

from utility_functions import manhattan_distance


class Character:
    """
    Base class for Players and Enemies. Can perform all the basic actions such as moving and attacking.
    """
    def __init__(self, name, x=0, y=0, attributes=None, status=None):
        """
        Initialize a Character object. This is only ever called through super() for Player and Enemies.
        :param name: Name of the character
        :param x: Character's x-coordinate
        :param y: Character's y-coordinate
        :param attributes: Dict containing the character's attributes.
        :param status: Dict containing a list of buffs and debuffs affecting this character

        The following attributes are also set at initialization:
        :hp: Character's HP represented as a list: [current, max], where max is equal to 2*VIT
        :mp: Character's MP, represented same as hp, but with an extra element, 'counter', which is incremented
             every turn and used to determine the character's passive MP regen, where max is equal to 2*WIS
        """
        self.name = name
        self.x = x
        self.y = y
        self.attributes = attributes if attributes is not None else {
            "str": 2,
            "dex": 2,
            "int": 2,
            "end": 2,
            "vit": 2,
            "wis": 2
        }
        self.hp = [self.attributes['vit'] * 2, self.attributes['vit'] * 2]
        self.mp = [self.attributes['wis'] * 2, self.attributes['wis'] * 2, 0]
        self.status = status if status is not None else {
            'buffs': list(),
            'debuffs': list()
        }

    def __str__(self):
        return f'{self.name} - ({self.x}, {self.y})'

    def __repr__(self):
        return f'{self.name} - ({self.x}, {self.y})'

    def move_up(self, steps=1):
        """Moves the character along the y-axis"""
        # Note that (0, 0) is the top left corner, so we subtract from  the y position to move up
        return self.x, self.y - steps

    def move_right(self, steps=1):
        """Moves the character along the x-axis"""
        return self.x + steps, self.y

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
                console_text.append(status.end_of_turn_effect(target=self, **status.params))
            status.turns_left -= 1
            if status.turns_left == 0:
                self.remove_status(status)

        return console_text

    def passive_mp_regen(self):
        """
        Character's will passively regenerate MP based on their WISDOM attribute. MP is stored as a list of three int's,
            [current, max, counter],
        where the counter variable is incremented every turn by a value based on the WISDOM value, and if it reaches
        a certain threshold, the character regenerates MP. If the character is already at max MP, the counter will be
        reset to 0 and nothing more will happen.
        Counter threshold is currently set to 20.
        """
        if self.mp[0] == self.mp[1]:
            self.mp[2] = 0
            return
        self.mp[2] += self.attributes['wis']
        if self.mp[2] >= 20:
            self.mp[0] = min(self.mp[0] + 1, self.mp[1])
            self.mp[2] = 0
        return

    def is_enemy(self):
        if self.__class__.__name__ == 'Enemy':
            return True
        return False

    def apply_defensive_combat_statuses(self, combat_dict):
        """
        Applies all the defensive combat statuses of this character when they are being attacked.
        :param combat_dict: A dict containing all the data points of the combat instance, e.g. the attacker, the target,
                            the damage being dealt, etc.
        :return: console_text, a list of all the new console text resulting from these status effects.
        """
        console_text = list()
        for status in self.status['buffs'] + self.status['debuffs']:
            if status.is_combat_status() and not status.offensive:
                console_text.append(status.combat_function(**combat_dict))

        return console_text


    def apply_attribute_changes(self):
        """
        Function to be called every time a character's attributes change, so as to update the rest of the character's
        stats accordingly.
        """
        # Only max values for HP and MP are updated at this time
        self.hp = [self.hp[0], self.attributes['vit'] * 2]
        self.mp = [self.mp[0], self.attributes['wis'] * 2, self.mp[2]]

