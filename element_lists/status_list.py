from math import ceil

from game_elements.status import Status


"""
Module for storing the list of every status and the possible effects.
"""

#### EFFECTS ####

def lesser_poison_effect(target):
    """Target loses 10% of their max HP, rounded up."""
    target.hp[0] -= ceil(0.1 * target.hp[1])


#### STATUSES ####

lesser_poison = Status(name='lesser_poison', type='debuff', duration=5,
                       end_of_turn_effect=lesser_poison_effect)

