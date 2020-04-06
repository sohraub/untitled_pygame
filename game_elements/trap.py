

class Trap:
    def __init__(self, x=0, y=0, name='', type='direct', function=None, trigger_prob=0.9, trigger_avoid_coeff=1):
        """
        Traps are objects that can be placed on boards, that will cause various affects once stepped on by either
        the player or an enemy.
        :param x: x-coordinate of the trap.
        :param y: y-coordinate of the trap.
        :param name: String used to identify the trap in the console text.
        :param type: 'direct' or 'debuff', to determine the logic in applying the trap effect.
        :param function: The function that is applied to the target of the trap.
        :param trigger_prob: Probability of the trap to trigger when stepped on.
        :param trigger_avoid_coeff: Coefficient for victim's dex attributed used to calculate the probability of the
                                    trap not triggering.
        """
        self.x = x
        self.y = y
        self.name = name
        self.type = type
        self.function = function
        self.trigger_prob = trigger_prob
        self.trigger_avoid_coeff = trigger_avoid_coeff


# Traps will be split into two categories, those that deal direct damage once, and those that inflict a debuff.
# We initialize two sets here for holding all of the trap types which fall into the first category. Since the logic for
# each type will be handled differently, when a trap is triggered we check to see which category it falls into, and
# call the appropriate function.

# DIRECT_DAMAGE_TRAPS = {'spike'}
DIRECT_DAMAGE_TRAPS = {}
DEBUFF_TRAPS = {'lesser poison'}

def generate_random_trap(coord):
    import random
    from copy import copy
    from element_lists.trap_list import TRAP_LIST

    trap = copy(random.choice(TRAP_LIST))
    trap.x = coord[0]
    trap.y = coord[1]

    return trap
