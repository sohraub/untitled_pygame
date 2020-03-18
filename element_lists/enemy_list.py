import random
import copy
from uuid import uuid4

from game_elements.enemy import Enemy


"""
Module containing every Enemy as well as lists to be randomly chosen from, based on tier.
"""


large_rat = Enemy(name='large_rat', hp=[8, 8], mp=[1, 1],
                  attributes={'str':3, 'dex':2, 'int': 1, 'end':3, 'vit':2, 'wis':1})

untitled_humanoid = Enemy(name='placeholder', hp=[10, 10], mp=[5, 5],
                          attributes={'str':4, 'dex':3, 'int':2, 'end':3, 'vit':2, 'wis':2})


# Enemies will be grouped by tier, and when enemies are generated, the Game class will pull randomly
# from the appropriately-tiered list.
tier_1 = [large_rat, untitled_humanoid]


def generate_new_enemy(x, y, tier):
    tier_mapping = {
        1: tier_1
    }
    new_enemy = copy.deepcopy(random.choice(tier_mapping[tier]))
    new_enemy.name = new_enemy.name + '_{}'.format(str(uuid4()))
    new_enemy.x = x
    new_enemy.y = y
    return new_enemy
