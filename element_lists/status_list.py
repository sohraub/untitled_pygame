from math import ceil

from game_elements.status import Status
from utility_functions import parse_description


"""
Module for storing the list of every status and the possible effects.
"""

#### EFFECTS ####

def lesser_poison_effect(target):
    """Target loses 10% of their max HP, rounded up."""
    damage = ceil(0.1 * target.hp[1])
    target.hp[0] = max(0, target.hp[0] - damage)
    if target.__class__.__name__ == 'Enemy':
        console_text = f'The {target.display_name} takes '
    else:
        console_text = f'You take '
    console_text += f'{damage} damage from being poisoned.'
    return console_text


#### STATUSES ####

lesser_poison = Status(name='Lesser Poison', type='debuff', duration=5,
                       description=parse_description('Take a small amount of poison damage every turn.'),
                       end_of_turn_effect=lesser_poison_effect)

