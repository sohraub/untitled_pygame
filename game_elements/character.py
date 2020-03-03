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

    def basic_attack(self, target, enemy_attack=False):
        """Character performs a basic attack on target. Logic is handled slightly differently if enemy is attacking."""
        # TODO: Might be worth creating separate attack functions for Player and Enemy
        # console_text is a list of strings that will be returned, to be printed in the console. It's initialized as
        # a list with just the empty string, and in most cases will just be a list of one string. If the enemy is killed
        # we also add death text to this list, so that both will be displayed on separate lines.
        console_text = ['']
        base_damage = max(self.attributes['str'] - target.attributes['end'], 1)
        base_accuracy = 70 + 5 * (self.attributes['dex'] - target.attributes['dex'])
        crit_chance = self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis'])
        if random.randint(0, 100) <= crit_chance:
            base_damage = 2 * base_damage
            console_text[0] += 'Critical hit! '
        elif random.randint(0, 100) >= base_accuracy:
            base_damage = 0
            console_text[0] += 'Miss! '
        if not enemy_attack:
            # Console text is different if attack is from the Player compared to an Enemy
            console_text[0] += 'You dealt {0} damage to {1}. '.format(base_damage, ' '.join(target.name.split('_')[0:-1]))
        else:
            console_text[0] += 'The {0} attacks you for {1} damage. '.format(' '.join(self.name.split('_')[0:-1]),
                                                                          base_damage)
        target.hp[0] = max(target.hp[0] - base_damage, 0)
        if target.hp[0] == 0 and not enemy_attack:
            from game_elements.enemy import death_phrases
            console_text.append(random.choice(death_phrases))
        return console_text
