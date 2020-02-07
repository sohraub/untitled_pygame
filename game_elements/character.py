import random
import math

from utility_functions import get_manhattan_distance


class Character:
    def __init__(self, name, x=0, y=0, hp=None, mp=None, attributes=None, status=None, move_speed=1, in_combat=False):
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
        self.move_speed = move_speed
        self.in_combat = in_combat

    def move_to(self, destination):
        if self.in_combat:
            if get_manhattan_distance((self.x, self.y), destination) > self.move_speed:
                return False
        self.x = destination[0]
        self.y = destination[1]

    def move_up(self, steps=1):
        # Note that (0, 0) is the top left corner, so we subtract from
        # the y position to move up
        self.move_to((self.x, self.y - steps))

    def move_right(self, steps=1):
        self.move_to((self.x + steps, self.y))

    def basic_attack(self, target, enemy_attack=False):
        console_text = ''
        base_damage = max(self.attributes['str'] - target.attributes['end'], 0)
        base_accuracy = 70 + 5 * (self.attributes['dex'] - target.attributes['dex'])
        crit_chance = self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis'])
        if random.randint(0, 100) <= crit_chance:
            base_damage = 2 * base_damage
            console_text += 'Critical hit! '
        elif random.randint(0, 100) >= base_accuracy:
            base_damage = 0
            console_text += 'Miss! '
        if not enemy_attack:
            console_text += 'You dealt {0} damage to {1}. '.format(base_damage, ' '.join(target.name.split('_')[0:-1]))
        else:
            console_text += 'The {0} attacks you for {1} damage. '.format(' '.join(self.name.split('_')[0:-1]), base_damage)
        target.hp[0] = max(target.hp[0] - base_damage, 0)
        if target.hp[0] == 0 and not enemy_attack:
            from game_elements.enemy import death_phrases
            console_text += random.choice(death_phrases)
        return console_text
