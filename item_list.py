import random
import copy

import item_effects
from game_elements.item import Item, Consumable, Equipment

"""
Module containing all of the items that can be loaded into a board.
"""

#### CONSUMABLES ####
small_hp_potion = Consumable(name='Small HP Potion',
                             description='A small potion you can drink to restore a bit of HP.',
                             effects=[item_effects.increase_hp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['HP +5', 'Thirst -3'], verb='drank')

small_mp_potion = Consumable(name='Small MP Potion',
                             description='A small potion you can drink to restore a bit of MP.',
                             effects=[item_effects.increase_mp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['MP +5', 'Thirst -3'], verb='drank')

apple = Consumable(name='Apple',
                   description='The fruit that needs no introduction.',
                   effects=[item_effects.improve_conditions],
                   parameters=[{'conditions':['hungry', 'thirsty'], 'values':[10, 1]}],
                   details=['Hunger -10', 'Thirst -1'], verb='ate')


#### LISTS OF CONSUMABLES ####
tier_1_c = [small_hp_potion, small_mp_potion, apple]


#### EQUIPPABLES ####
rusty_sword = Equipment(name='Rusty Sword',
                        description='This sword has seen better days, but could still do some damage.',
                        slot='weapon', off_rating=2, stat_req={'str': 2, 'dex': 2})

short_sword = Equipment(name='Short Sword',
                        description='Looks quite sharp, although it does lack much reach.',
                        slot='weapon', off_rating=3, stat_req={'str': 2, 'dex': 3})

leather_cap = Equipment(name='Leather Cap',
                        description="Doesn't offer much protection, but better than nothing.", slot='head',
                        def_rating=1)

#### LISTS OF EQUIPPABLES ####
# tier_1_e = [rusty_sword, leather_cap]
tier_1_e = [rusty_sword, short_sword]

def generate_random_item(tier, type='both'):
    """
    Function which returns a copy of a random item based on the tier and type.

    :param tier: An int, signifying the tier of item to pull from.
    :param type: A string, which can be either 'consumable', 'equipment', or 'both'.
    """
    if type not in {'consumable', 'equipment', 'both'}:
        raise Exception(f'Tried to generate a random item with invalid type, {type}.')
    tier_mapping = {
        '1_consumable': tier_1_c,
        '1_equipment': tier_1_e,
        '1_both': tier_1_c + tier_1_e
    }
    new_item = copy.deepcopy(random.choice(tier_mapping[f'{tier}_{type}']))
    return new_item