import random
import copy

import item_effects
from game_elements.item import Item, Consumable

small_hp_potion = Consumable(name='Small HP Potion',
                             description='A small potion which restores a bit of HP and slightly quenches thirst.',
                             effects=[item_effects.increase_hp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}])

small_mp_potion = Consumable(name='Small MP Potion',
                             description='A small potion which restores a bit of MP and slightly quenches thirst.',
                             effects=[item_effects.increase_mp, item_effects.improve_conditions],
                             parameters=[{'value':5}, {'conditions':['thirsty'], 'values':[3]}])

apple = Consumable(name='Apple',
                   description='The fruit that needs no introduction. Satisfies hunger and slightly quenches thirst.',
                   effects=[item_effects.improve_conditions],
                   parameters=[{'conditions':['hungry', 'thirsty'], 'values':[10, 5]}])

tier_1 = [small_hp_potion, small_mp_potion, apple]

def generate_random_item(tier):
    tier_mapping = {
        1: tier_1
    }
    new_item = copy.deepcopy(random.choice(tier_mapping[tier]))
    return new_item