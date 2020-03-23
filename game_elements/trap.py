

class Trap:
    def __init__(self, x=0, y=0, type='spike', category='direct', function=None, trigger_prob=0.9,
                 trigger_avoid_coeff=1, def_rating_coeff=1):
        """
        Traps are objects that can be placed on boards, that will cause various affects once stepped on by either
        the player or an enemy.
        :param x: x-coordinate of the trap
        :param y: y-coordinate of the trap
        :param type: String representing the type of trap, e.g. spike trap, poison gas trap, etc. This will also
                     be used to determine the category of trap (direct damage, debuff, etc.)
        :param category: String representing the trap category.
        :param function: The function that is applied to the target of the trap.
        :param trigger_prob: Probability of the trap to trigger when stepped on.
        :param trigger_avoid_coeff: Coefficient for victim's dex attributed used to calculate the probability of the
                                    trap not triggering.
        """
        self.x = x
        self.y = y
        self.type = type
        self.category = category
        self.function = function
        self.trigger_prob = trigger_prob
        self.trigger_avoid_coeff = trigger_avoid_coeff


# Traps will be split into two categories, those that deal direct damage once, and those that inflict a debuff.
# We initialize two sets here for holding all of the trap types which fall into the first category. Since the logic for
# each type will be handled differently, when a trap is triggered we check to see which category it falls into, and
# call the appropriate function.

DIRECT_DAMAGE_TRAPS = {'spike'}
DEBUFF_TRAPS = {'l_poison'}

def generate_random_trap(coord):
    import random
    from element_lists.trap_list import trap_map
    type = random.choice(list(DIRECT_DAMAGE_TRAPS) + list(DEBUFF_TRAPS))
    if type in DIRECT_DAMAGE_TRAPS:
        category = 'direct'
    else:
        category = 'debuff'
    trap_config = trap_map[type]
    return Trap(x=coord[0], y=coord[1], type=type, category=category, function=trap_config['function'],
                trigger_prob=trap_config['trigger_prob'], trigger_avoid_coeff=trap_config['trigger_avoid_coeff'])
