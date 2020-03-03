import random
import copy

import item_effects
from game_elements.item import Item, Consumable

"""
Module containing all of the items that can be loaded into a board.
"""

#### CONSUMABLES ####
small_hp_potion = Consumable(name='Small HP Potion',
                             description='A small potion you can drink to restore a bit of HP.',
                             effects=[item_effects.increase_hp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['HP +5', 'Thirst -3'])

small_mp_potion = Consumable(name='Small MP Potion',
                             description='A small potion you can drink to restore a bit of MP.',
                             effects=[item_effects.increase_mp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['MP +5', 'Thirst -3'])

apple = Consumable(name='Apple',
                   description='The fruit that needs no introduction.',
                   effects=[item_effects.improve_conditions],
                   parameters=[{'conditions':['hungry', 'thirsty'], 'values':[10, 1]}],
                   details=['Hunger -10', 'Thirst -1'])


#### LISTS OF CONSUMABLES ####
tier_1 = [small_hp_potion, small_mp_potion, apple]

def generate_random_item(tier):
    """Function which returns a copy of a random item based on the tier."""
    tier_mapping = {
        1: tier_1
    }
    new_item = copy.deepcopy(random.choice(tier_mapping[tier]))
    return new_item