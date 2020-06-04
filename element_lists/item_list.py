import random
import copy

from item_effects import *
from game_elements.item import Item, Consumable, Equipment

"""
Module containing all of the items that can be loaded into a board.
"""

#### CONSUMABLES ####
small_hp_potion = Consumable(name='Small HP Potion',
                             description='A small potion you can drink to restore a bit of HP.',
                             effects=[increase_hp, improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['HP +5', 'Thirst -3'],
                             console_text='You drink the Small HP Potion.')

small_mp_potion = Consumable(name='Small MP Potion',
                             description='A small potion you can drink to restore a bit of MP.',
                             effects=[increase_mp, improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}],
                             details=['MP +5', 'Thirst -3'],
                             console_text='You drink the Small MP Potion.')

apple = Consumable(name='Apple',
                   description='The fruit that needs no introduction.',
                   effects=[improve_conditions],
                   parameters=[{'conditions':['hungry', 'thirsty'], 'values':[10, 1]}],
                   details=['Hunger -10', 'Thirst -1'],
                   console_text='You eat the apple.')

questionable_liquid = Consumable(name='Questionable Liquid',
                                 description='Whatever is in this flask might be passable as water, but its smell does'
                                             ' not inspire confidence in its safety.',
                                 effects=[improve_conditions, chance_to_poison],
                                 parameters=[{'conditions':['thirsty'], 'values':[15]},
                                             {'probability': 5, 'status_duration': 3}],
                                 details=['Thirst -15', '5% Chance to Poison'],
                                 console_text='You nervously down the questionable liquid.')

bedroll = Consumable(name='Bedroll',
                     description='The opportunity for respite, to forget about the situation in which you find yourself,'
                                 ' and to recharge your resolve to push forward.',
                     effects=[improve_conditions, increase_hp, increase_mp],
                     parameters=[{'conditions':['tired', 'hungry', 'thirsty'], 'values':[40, -10, -10],},
                                 {'value': 1000}, {'value': 1000}],
                     details=['Tiredness -40','Hunger +10', 'Thirst +10','Fully Restore HP and MP',
                              "Can't be used if any enemies are around"],
                     prereqs=['no_enemies_on_board'], console_text='You have a much-needed rest on the bedroll.')

#### LISTS OF CONSUMABLES ####
tier_1_c = [small_hp_potion, small_mp_potion, apple, questionable_liquid, bedroll]


#### EQUIPPABLES ####
rusty_sword = Equipment(name='Rusty Sword',
                        description='This sword has seen better days, but could still do some damage.',
                        slot='weapon', off_rating=2, stat_req={'str': 2, 'dex': 2})

short_sword = Equipment(name='Short Sword',
                        description='Looks quite sharp, although it does lack much reach.',
                        slot='weapon', off_rating=3, stat_req={'str': 2, 'dex': 3})

old_leather_cap = Equipment(name='Old Leather Cap',
                            description="Doesn't offer much protection, but better than nothing.", slot='head',
                            def_rating=1)

old_leather_tunic = Equipment(name='Old Leather Tunic', description="Suppose it beats being completely exposed.",
                              slot='body', def_rating=3)

old_leather_boots = Equipment(name='Old Leather Boots', description="The soles are falling apart...",
                              slot='feet', def_rating=1)

old_leather_gloves = Equipment(name='Old Leather Gloves',
                               description="Going to assume those finger-holes are there by design.", slot='hands',
                               def_rating=1)

#### LISTS OF EQUIPPABLES ####
tier_1_e = [rusty_sword, old_leather_cap, short_sword, old_leather_boots, old_leather_gloves, old_leather_tunic]

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