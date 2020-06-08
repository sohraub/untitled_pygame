import random
import copy
from uuid import uuid4

from game_elements.enemy import Enemy


"""
Module containing every Enemy as well as lists to be randomly chosen from, based on tier.
"""


large_rat = Enemy(display_name='Large Rat', name='large_rat',
                  attributes={'str':5, 'dex':2, 'int': 1, 'end':3, 'vit':5, 'wis':1,},
                  flavour_text='Not used to seeing rats this big. The smell of decay and the patchiness of its fur '
                               'suggests some kind of disease.',
                  level_up_dict={'str':0.8, 'dex':0.4, 'vit':0.8})

skeleton = Enemy(display_name='Skeleton', name='skeleton',
                 attributes={'str':6, 'dex':3, 'int':2, 'end':3, 'vit':6, 'wis':2},
                 flavour_text="The stories you've heard don't do the real thing any justice. Rotten pieces of meat "
                              "are visible and pungent, still attached to the bone.",
                 level_up_dict={'str':0.8, 'dex':0.4, 'vit':0.8})


# Enemies will be grouped by tier, and when enemies are generated, the Game class will pull randomly
# from the appropriately-tiered list.
tier_1 = [large_rat, skeleton]


