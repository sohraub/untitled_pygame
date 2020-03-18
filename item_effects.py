"""
Module that stores all the possible effects an item can have, which are imported into item list on the initialization
of items.
"""

def increase_hp(target, value):
    """Increase the hp of 'target' by 'value'"""
    if value >= 0:
        target.hp[0] = min(target.hp[0] + value, target.hp[1])
    else:
        target.hp[0] = max(target.hp[0] - value, 0)

def increase_mp(target, value):
    """Increase the mp of 'target' by 'value'"""
    if value >= 0:
        target.mp[0] = min(target.mp[0] + value, target.mp[1])
    else:
        target.mp[0] = max(target.mp[0] - value, 0)

def improve_conditions(target, conditions, values):
    """Improves conditions by the associated value. Can effect multiple conditions at once."""
    for condition, value in zip(conditions, values):
        if value >= 0:
            target.conditions[condition][0] = min(target.conditions[condition][0] + value,
                                                  target.conditions[condition][1])
        else:
            target.conditions[condition][0] = max(target.conditions[condition][0] - value, 0)
