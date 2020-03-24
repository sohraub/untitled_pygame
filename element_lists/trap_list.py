from game_elements.trap import Trap

"""
Module for storing the list of all of the trap effects. The Trap class will have an attribute called 'type', which
stores a string that gets mapped to the corresponding function for applying the effect of that trap.
"""


def spike_trap(target):
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

def lesser_poison_trap(target):
    """
    Applies the lesser_poison status to the target.
    :return: A string signifying the status suffered to be displayed in the console.
    """
    from element_lists.status_list import lesser_poison
    target.apply_status(lesser_poison)
    return 'poisoned'

# Map to store all of the info specific to each type of trap.
trap_map = {
    'spike': {
        'function': spike_trap,
        'trigger_prob': 0.8,
        'trigger_avoid_coeff': 1
    },
    'lesser poison': {
        'function': lesser_poison_trap,
        'trigger_prob': 0.7,
        'trigger_avoid_coeff': 0.5
    }

}

