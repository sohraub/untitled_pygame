import random
import copy
from uuid import uuid4

from game_elements.enemy import Enemy


"""
Module containing every Enemy as well as lists to be randomly chosen from, based on tier.
"""


large_rat = Enemy(display_name='Large Rat', name='large_rat', hp=[8, 8], mp=[1, 1, 0],
                  attributes={'str':3, 'dex':2, 'int': 1, 'end':3, 'vit':2, 'wis':1})

zombie = Enemy(display_name='Zombie', name='zombie', hp=[10, 10], mp=[5, 5, 0],
               attributes={'str':4, 'dex':3, 'int':2, 'end':3, 'vit':2, 'wis':2})


# Enemies will be grouped by tier, and when enemies are generated, the Game class will pull randomly
# from the appropriately-tiered list.
tier_1 = [large_rat, zombie]


