from copy import copy

from game_elements.trap import Trap

"""
Module for storing the list of all of the traps and trap effects.
"""

#### TRAP EFFECTS ####
def trigger_spike_trap(target):
    """
    Deals direct damage to the target, based on 20% of their maximum health.
    :param target: A Player or Enemy which stepped on the trap.
    :return: damage, the damage done to the target.
             console_text, new text to be displayed on the console.
    """
    damage = 0.2 * target.hp[1]
    if target.__class__.__name__ == 'Player':
        damage -= target.def_rating
    return int(damage)

def trigger_lesser_poison_trap(target):
    """
    Applies the lesser_poison status to the target.
    :return: A string signifying the status suffered to be displayed in the console.
    """
    from element_lists.status_list import lesser_poison
    target.apply_status(copy(lesser_poison))
    return 'poisoned'


#### TRAPS ####
spike_trap = Trap(type='direct', name='spike', function=trigger_spike_trap, trigger_prob=0.7, trigger_avoid_coeff=1)
lesser_poison_trap = Trap(type='debuff', name='lesser poison', function=trigger_lesser_poison_trap, trigger_prob=0.8,
                          trigger_avoid_coeff=0.5)


# TRAP_LIST = [spike_trap, lesser_poison_trap]
TRAP_LIST = [lesser_poison_trap]
