import random
import copy
from uuid import uuid4

from game_elements.enemy import Enemy


"""
Module containing every Enemy as well as lists to be randomly chosen from, based on tier.
"""


large_rat = Enemy(display_name='Large Rat', name='large_rat',
                  attributes={'str':5, 'dex':2, 'int': 1, 'end':3, 'vit':5, 'wis':1})

zombie = Enemy(display_name='Zombie', name='zombie',
               attributes={'str':6, 'dex':3, 'int':2, 'end':3, 'vit':6, 'wis':2})


# Enemies will be grouped by tier, and when enemies are generated, the Game class will pull randomly
# from the appropriately-tiered list.
tier_1 = [large_rat, zombie]


